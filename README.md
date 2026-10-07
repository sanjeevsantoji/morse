# Morse Code Analyzer

A Flask-based Morse code app for encoding, decoding, analyzing, and visualizing Morse signals. It also includes image-based Morse extraction support to detect Morse patterns from uploaded images.

## Features

- Encode plain text into Morse code
- Decode Morse code back into text
- Analyze Morse code statistics and structure
- View the Morse code reference table and tree
- Generate Morse code visual images
- Extract Morse patterns from uploaded images
- Modern web interface in Flask

## Project Structure

```text
morse/
├── app.py                 # Flask application and API routes
├── morse_engine.py        # Core Morse encoding/decoding logic
├── image_processor.py     # Image processing for Morse extraction
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Frontend UI
└── README.md
```

## Tech Stack

- Python 3
- Flask
- Pillow
- NumPy

## Installation

1. Clone or open the project folder.
2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Encode text

- Method: `POST`
- Route: `/api/encode`
- Body:

```json
{
  "text": "HELLO WORLD"
}
```

Returns the encoded Morse string.

### Decode Morse

- Method: `POST`
- Route: `/api/decode`
- Body:

```json
{
  "morse": ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
}
```

Returns the decoded text.

### Analyze Morse

- Method: `POST`
- Route: `/api/analyze`
- Body:

```json
{
  "morse": ".... . .-.. .-.. ---"
}
```

Returns statistics such as dots, dashes, unique codes, and decoded text.

### Full Morse table

- Method: `GET`
- Route: `/api/table`

Returns the complete Morse reference table.

### Morse tree

- Method: `GET`
- Route: `/api/tree`

Returns the Morse code binary tree structure.

### Image processing

- Method: `POST`
- Route: `/api/process-image`
- Form field: `image`

Uploads an image and attempts to detect Morse code patterns from it.

### Generate Morse image

- Method: `POST`
- Route: `/api/generate-image`
- Body:

```json
{
  "morse": ".... . .-.. .-.. ---"
}
```

Returns a generated PNG image of the Morse code.

## Notes

- The image extraction feature works best with clear black/dark signal patterns on a light background.
- Morse strings are interpreted using standard International Morse code.
- Character spacing and word separators are supported using normal Morse formatting conventions.

## License

This project is provided as-is for educational and personal use.
