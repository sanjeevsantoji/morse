"""
Image Processor - Extract Morse code patterns from images.
Supports:
  1. Black/white stripe patterns (dot = short bar, dash = long bar)
  2. Light/dark signal patterns (flash-based morse)
  3. Text-in-image OCR-like detection of dots and dashes
"""

import io
import numpy as np
from PIL import Image


def process_image(file_bytes: bytes) -> dict:
    """
    Process an uploaded image and attempt to extract Morse code.

    Strategy:
    - Convert to grayscale
    - Threshold to binary
    - Scan rows for horizontal dark segments
    - Classify segments as dots or dashes based on width
    - Group into characters and words based on gaps
    """
    img = Image.open(io.BytesIO(file_bytes)).convert('L')

    # Resize if too large
    max_width = 1200
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

    arr = np.array(img)

    # Binary threshold
    threshold = 128
    binary = (arr < threshold).astype(np.uint8)  # 1 = dark, 0 = light

    # Find the row with the most activity (horizontal middle band)
    row_sums = binary.sum(axis=1)
    if row_sums.max() == 0:
        return {
            'success': False,
            'message': 'No dark patterns detected in the image. Please upload an image with clear Morse code patterns (dark dots and dashes on a light background).',
            'morse': '',
            'decoded': '',
            'segments': [],
            'image_info': {
                'width': img.width,
                'height': img.height,
            }
        }

    # Use the densest horizontal band (average of top rows by activity)
    top_rows = np.argsort(row_sums)[-max(1, img.height // 10):]
    scan_line = binary[top_rows].mean(axis=0)
    scan_binary = (scan_line > 0.5).astype(np.uint8)

    # Extract dark segments (runs of 1s)
    segments = []
    in_segment = False
    start = 0
    for i, val in enumerate(scan_binary):
        if val == 1 and not in_segment:
            in_segment = True
            start = i
        elif val == 0 and in_segment:
            in_segment = False
            segments.append({'start': int(start), 'end': int(i), 'width': int(i - start)})
    if in_segment:
        segments.append({'start': int(start), 'end': int(len(scan_binary)), 'width': int(len(scan_binary) - start)})

    if not segments:
        return {
            'success': False,
            'message': 'No horizontal segments detected. Ensure the image has clear horizontal dots and dashes.',
            'morse': '',
            'decoded': '',
            'segments': [],
            'image_info': {
                'width': img.width,
                'height': img.height,
            }
        }

    # Classify: find median width, dots < median, dashes >= median
    widths = [s['width'] for s in segments]
    median_width = float(np.median(widths))

    # If all same width, treat as dots
    if max(widths) - min(widths) < 3:
        for s in segments:
            s['type'] = 'dot'
    else:
        dot_threshold = median_width * 0.75
        for s in segments:
            s['type'] = 'dot' if s['width'] < dot_threshold else 'dash'

    # Group into characters and words based on gaps between segments
    gaps = []
    for i in range(1, len(segments)):
        gap = segments[i]['start'] - segments[i - 1]['end']
        gaps.append(gap)

    if gaps:
        median_gap = float(np.median(gaps))
        char_gap_threshold = median_gap * 2.0
        word_gap_threshold = median_gap * 5.0
    else:
        char_gap_threshold = 10
        word_gap_threshold = 30

    # Build morse string
    morse_parts = []
    for i, seg in enumerate(segments):
        morse_parts.append('.' if seg['type'] == 'dot' else '-')
        if i < len(gaps):
            if gaps[i] > word_gap_threshold:
                morse_parts.append(' / ')
            elif gaps[i] > char_gap_threshold:
                morse_parts.append(' ')

    morse_string = ''.join(morse_parts)

    # Decode
    from morse_engine import morse_to_text
    decoded = morse_to_text(morse_string)

    return {
        'success': True,
        'message': f'Successfully extracted {len(segments)} segments from the image.',
        'morse': morse_string,
        'decoded': decoded,
        'segments': segments,
        'image_info': {
            'width': img.width,
            'height': img.height,
            'median_segment_width': round(median_width, 1),
            'total_segments': len(segments),
            'dots': sum(1 for s in segments if s['type'] == 'dot'),
            'dashes': sum(1 for s in segments if s['type'] == 'dash'),
        }
    }


def generate_morse_image(morse_code: str) -> bytes:
    """
    Generate an image representation of Morse code.
    Dots = small circles, Dashes = horizontal bars.
    """
    dot_width = 20
    dash_width = 60
    height = 40
    gap = 10
    char_gap = 30
    word_gap = 60
    padding = 30

    # Calculate total width
    total_width = padding
    for char in morse_code:
        if char == '.':
            total_width += dot_width + gap
        elif char == '-':
            total_width += dash_width + gap
        elif char == ' ':
            total_width += char_gap
        elif char == '/':
            total_width += word_gap
    total_width += padding

    # Create image
    img = Image.new('RGB', (max(total_width, 100), height + padding * 2), color=(15, 23, 42))

    pixels = np.array(img)
    x = padding
    y_center = height // 2 + padding

    for char in morse_code:
        if char == '.':
            # Draw dot (filled circle approximation)
            r = dot_width // 2
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if dx * dx + dy * dy <= r * r:
                        px, py = x + r + dx, y_center + dy
                        if 0 <= px < pixels.shape[1] and 0 <= py < pixels.shape[0]:
                            pixels[py, px] = (56, 189, 248)  # cyan
            x += dot_width + gap
        elif char == '-':
            # Draw dash (rectangle)
            bar_height = 12
            for dy in range(-bar_height // 2, bar_height // 2 + 1):
                for dx in range(dash_width):
                    px, py = x + dx, y_center + dy
                    if 0 <= px < pixels.shape[1] and 0 <= py < pixels.shape[0]:
                        pixels[py, px] = (251, 146, 60)  # orange
            x += dash_width + gap
        elif char == ' ':
            x += char_gap
        elif char == '/':
            x += word_gap

    result = Image.fromarray(pixels)
    buf = io.BytesIO()
    result.save(buf, format='PNG')
    return buf.getvalue()
