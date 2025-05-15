# AutoToC: Automated PDF Table of Contents Extractor

## Overview

AutoToC is a powerful tool that automatically extracts Tables of Contents (TOC) from PDF documents using AI vision technology. This tool can identify and preserve the structure, formatting, and details of complex document hierarchies without manual intervention.

## Features

- **AI-Powered Extraction**: Leverages OpenAI's GPT-4 vision capabilities to intelligently identify TOC content
- **Format Preservation**: Maintains original document formatting including case numbers, dotted leaders, and page numbers
- **Command-Line Interface**: Simple to use from the terminal with clear output and progress indicators
- **Performance Monitoring**: Built-in timing for processing steps to help optimize extraction
- **Preview Functionality**: Shows a sample of the extracted TOC after processing
- **Flexible Output**: Saves results to customizable locations

## Requirements

- Python 3.6+
- Dependencies:
  - openai
  - python-dotenv
  - pdf2image
  - opencv-python-headless
  - pytesseract
  - PyMuPDF

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AutoToC.git
   cd AutoToC
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Command Line

Extract a TOC from a PDF file:
```
python extract_toc.py path/to/your/document.pdf [output/path.txt]
```

If no output path is specified, the TOC will be saved to `toc/[document_name]_toc.txt`.

### As a Module

You can also use the extractor in your own Python scripts:

```python
from pdf_toc_extractor import extract_table_of_contents

toc = extract_table_of_contents("path/to/document.pdf", "output/path.txt")
print(toc)
```

## How It Works

1. The PDF's initial pages (up to 20 by default) are converted to high-resolution images
2. These images are encoded and sent to OpenAI's Vision API
3. A specialized prompt instructs the AI to extract only the actual table of contents
4. The extracted TOC is formatted and saved to the specified output file

## Limitations

- Processes only the first 20 pages of a PDF by default (adjustable in the code)
- Requires an OpenAI API key with access to GPT-4 vision capabilities
- Performance depends on PDF quality and clarity

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
