"""
Morse Code Engine - Core encoding, decoding, and analysis logic.
"""

# International Morse Code mapping
CHAR_TO_MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...',  ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.',  '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-','@': '.--.-.', ' ': '/'
}

MORSE_TO_CHAR = {v: k for k, v in CHAR_TO_MORSE.items()}


def text_to_morse(text: str) -> str:
    """Convert plain text to Morse code."""
    result = []
    for char in text.upper():
        if char in CHAR_TO_MORSE:
            result.append(CHAR_TO_MORSE[char])
        else:
            result.append('?')
    return ' '.join(result)


def morse_to_text(morse: str) -> str:
    """Convert Morse code to plain text."""
    words = morse.strip().split(' / ')
    decoded_words = []
    for word in words:
        chars = word.strip().split(' ')
        decoded_word = ''
        for c in chars:
            c = c.strip()
            if c == '':
                continue
            if c in MORSE_TO_CHAR:
                decoded_word += MORSE_TO_CHAR[c]
            else:
                decoded_word += '□'
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)


def analyze_morse(morse: str) -> dict:
    """Analyze a Morse code string and return statistics."""
    dots = morse.count('.')
    dashes = morse.count('-')
    separators = morse.count('/')
    total_symbols = dots + dashes

    # Break into individual codes
    codes = [c.strip() for c in morse.replace('/', ' ').split(' ') if c.strip()]
    unique_codes = set(codes)

    # Decode
    decoded = morse_to_text(morse)

    # Character frequency in decoded text
    char_freq = {}
    for ch in decoded:
        if ch != ' ':
            char_freq[ch] = char_freq.get(ch, 0) + 1

    # Morse length per character
    morse_lengths = {}
    for code in codes:
        if code in MORSE_TO_CHAR:
            char = MORSE_TO_CHAR[code]
            morse_lengths[char] = len(code)

    # Average morse length
    avg_length = sum(len(c) for c in codes) / len(codes) if codes else 0

    # Longest / shortest codes
    longest = max(codes, key=len) if codes else ''
    shortest = min(codes, key=len) if codes else ''

    return {
        'decoded_text': decoded,
        'total_dots': dots,
        'total_dashes': dashes,
        'dot_dash_ratio': round(dots / dashes, 2) if dashes > 0 else dots,
        'total_symbols': total_symbols,
        'total_characters': len(codes),
        'total_words': separators + 1 if codes else 0,
        'unique_characters': len(unique_codes),
        'average_code_length': round(avg_length, 2),
        'longest_code': longest,
        'longest_code_char': MORSE_TO_CHAR.get(longest, '?'),
        'shortest_code': shortest,
        'shortest_code_char': MORSE_TO_CHAR.get(shortest, '?'),
        'character_frequency': char_freq,
        'morse_lengths': morse_lengths,
    }


def get_morse_tree() -> dict:
    """Return the Morse code binary tree structure for visualization."""
    tree = {'label': 'START', 'children': {}}

    for char, code in CHAR_TO_MORSE.items():
        if char == ' ':
            continue
        node = tree
        for symbol in code:
            if symbol not in node['children']:
                node['children'][symbol] = {'label': '', 'children': {}}
            node = node['children'][symbol]
        node['label'] = char

    return tree


def get_full_table() -> list:
    """Return the full Morse code reference table."""
    table = []
    for char, code in sorted(CHAR_TO_MORSE.items()):
        if char == ' ':
            display = 'SPACE'
        else:
            display = char
        table.append({
            'character': display,
            'morse': code,
            'length': len(code),
            'dots': code.count('.'),
            'dashes': code.count('-'),
        })
    return table
