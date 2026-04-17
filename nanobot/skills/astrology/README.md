# Astrology Skill

Fetch and analyze celebrity natal charts from astro-charts.com using browser automation and OCR.

## Overview

This skill automates the process of fetching celebrity natal charts from astro-charts.com, extracting birth information using OCR, and generating comprehensive astrological analyses using graph-based structural prompts.

## Features

- 🌐 **Browser Automation**: Navigate to astro-charts.com and capture full page screenshots
- 🔍 **OCR Text Extraction**: Extract birth information from screenshots using Tesseract OCR
- 📊 **Data Parsing**: Parse and extract name, birth date, and birth time from OCR text
- 📈 **Chart Analysis**: Generate graph-based structural prompts for natal chart analysis
- ✨ **Comprehensive Analysis**: Provide detailed astrological interpretations

## Installation

### Prerequisites

1. **agent-browser**: Browser automation tool
2. **Tesseract OCR**: Text extraction from images
3. **horoscope-fetcher**: Natal chart data fetching and analysis

### Install Tesseract OCR

**macOS**:
```bash
brew install tesseract
```

**Ubuntu/Debian**:
```bash
sudo apt-get install tesseract-ocr
```

**Windows**:
Download from https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Basic Usage

```bash
# Analyze Elon Musk's natal chart
python3 scripts/astrology.py analyze "elon-musk"

# Analyze John Lennon's natal chart
python3 scripts/astrology.py analyze "john-lennon"
```

### Advanced Usage

```bash
# Run with headed browser (for debugging)
python3 scripts/astrology.py analyze "elon-musk" --headed

# Use manual data entry (skip OCR)
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, Gauteng, South Africa"

# Custom output directory
python3 scripts/astrology.py analyze "elon-musk" --output-dir ./my_charts
```

## Output

The skill generates the following outputs in the output directory:

1. **Screenshot**: `{name}_chart.png` - Full page screenshot of the natal chart
2. **OCR Text**: `{name}_ocr.txt` - Extracted text from the screenshot
3. **Parsed Data**: `{name}_parsed.json` - Parsed birth information
4. **Graph Prompt**: `{name}_graph_prompt.txt` - Graph-based structural prompt
5. **Analysis**: `{name}_analysis.md` - Comprehensive astrological analysis

## Workflow

```
1. Navigate to astro-charts.com
   ↓
2. Capture full page screenshot
   ↓
3. Extract text using OCR
   ↓
4. Parse birth information
   ↓
5. Generate graph-based structural prompt
   ↓
6. Provide comprehensive analysis
```

## Examples

### Example 1: Elon Musk

```bash
python3 scripts/astrology.py analyze "elon-musk"
```

Output files:
- `elon-musk_chart.png`
- `elon-musk_ocr.txt`
- `elon-musk_parsed.json`
- `elon-musk_graph_prompt.txt`
- `elon-musk_analysis.md`

### Example 2: John Lennon

```bash
python3 scripts/astrology.py analyze "john-lennon" --headed
```

## Troubleshooting

### OCR Fails

If OCR fails to extract birth information:

1. Use `--headed` to visually verify the screenshot
2. Try manual data entry with `--skip-ocr`
3. Check screenshot quality in the output directory
4. Ensure Tesseract OCR is properly installed

### Browser Navigation Fails

If browser navigation fails:

1. Check internet connection
2. Verify the celebrity name is correct
3. Use `--headed` to see what's happening
4. Check if astro-charts.com is accessible

### Chart Generation Fails

If chart generation fails:

1. Verify parsed birth data is correct
2. Check horoscope-fetcher skill is properly installed
3. Try manual data entry with `--skip-ocr`

## Supported Celebrities

The skill works with any celebrity available on astro-charts.com. Common examples include:

- elon-musk
- john-lennon
- oprah-winfrey
- steve-jobs
- albert-einstein
- marilyn-monroe

To find more celebrities, visit https://astro-charts.com/persons/

## Technical Details

### OCR Technology

The skill uses Tesseract OCR for text extraction. Tesseract is an open-source OCR engine developed by Google that supports over 100 languages.

### Graph-Based Analysis

The skill uses a graph-based structural framework for natal chart analysis:
- **Nodes**: Represent astrological elements (planets, signs, houses, aspects, retrogrades)
- **Edges**: Represent relationships (harmony/challenge of aspects, sign traits, planetary characteristics)
- **Graph Traversal**: Enables systematic analysis from core elements to extended features

### Browser Automation

The skill uses agent-browser for browser automation, which provides:
- Headless and headed browser modes
- Full page screenshot capture
- Cross-platform support (macOS, Linux, Windows)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This skill is part of the nanobot project.

## Credits

- **astro-charts.com**: Source of celebrity natal charts
- **Tesseract OCR**: Text extraction technology
- **horoscope-fetcher**: Natal chart data fetching and analysis
- **agent-browser**: Browser automation tool

## Changelog

### Version 1.0.0 (2026-03-16)
- ✅ Initial release
- ✅ Browser automation for astro-charts.com
- ✅ Screenshot capture functionality
- ✅ OCR text extraction
- ✅ Data parsing for birth information
- ✅ Integration with horoscope-fetcher
- ✅ Graph-based structural prompt generation
- ✅ Comprehensive astrological analysis
