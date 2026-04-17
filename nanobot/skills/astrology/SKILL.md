---
name: astrology
description: Fetch and analyze celebrity natal charts from astro-charts.com using browser automation and OCR. Use when the user needs to (1) Get celebrity birth chart data, (2) Analyze famous people's astrological charts, (3) Extract birth information from astro-charts.com, or (4) Generate comprehensive astrological analysis for celebrities.
---

# Astrology

Fetch and analyze celebrity natal charts from astro-charts.com using browser automation and OCR.

## Features

- **Browser Automation**: Navigate to astro-charts.com and capture full page screenshots
- **OCR Text Extraction**: Extract birth information from screenshots using OCR
- **Data Parsing**: Parse and extract name, birth date, and birth time from OCR text
- **Chart Analysis**: Generate graph-based structural prompts for natal chart analysis
- **Comprehensive Analysis**: Provide detailed astrological interpretations using LLM

## Usage

### Basic Usage

```bash
# Analyze Elon Musk's natal chart
python3 scripts/astrology.py analyze "elon-musk"

# Analyze John Lennon's natal chart
python3 scripts/astrology.py analyze "john-lennon"

# Analyze with custom output directory
python3 scripts/astrology.py analyze "elon-musk" --output-dir ./output
```

### Parameters

#### analyze Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Celebrity name (URL slug format, e.g., "elon-musk") |
| `--output-dir` | string | No | Output directory for screenshots and results (default: ./output) |
| `--headed` | flag | No | Run browser in headed mode (default: false) |
| `--skip-ocr` | flag | No | Skip OCR and use manual data entry |
| `--time` | string | No | Manual birth time (format: YYYY-MM-DD HH:MM:SS) |
| `--address` | string | No | Manual birth location |
| `--latitude` | float | No | Manual latitude |
| `--longitude` | float | No | Manual longitude |

## Workflow

The astrology skill follows this workflow:

1. **Browser Navigation**: Navigate to `https://astro-charts.com/persons/chart/{name}/`
2. **Screenshot Capture**: Capture full page screenshot of the natal chart
3. **OCR Extraction**: Extract text from screenshot using OCR
4. **Data Parsing**: Parse name, birth date, and birth time from OCR text
5. **Generate graph structure prompt**: Use horoscope-fetcher gen_analyze_chart_graph_prompt to generate graph-based structural prompt
6. **Analysis**: 根据上面的prompt进行星盘分析 从三大巨头开始，逐步扩展到宫位、行星群、关键单星 使用富有哲思和洞见的占星语言 按照图结构遍历，确保分析逻辑清晰 不要在最终分析中提及"节点"、"边"、"图结构"等技术术语

## Examples

### Example 1: Analyze Elon Musk's Chart

```bash
python3 scripts/astrology.py analyze "elon-musk"
```

This will:
1. Navigate to https://astro-charts.com/persons/chart/elon-musk/
2. Capture full page screenshot
3. Extract birth information using OCR
4. Generate graph-based structural prompt
5. Provide comprehensive analysis

### Example 2: Analyze with Headed Browser

```bash
python3 scripts/astrology.py analyze "john-lennon" --headed
```

### Example 3: Manual Data Entry (Skip OCR)

```bash
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, Gauteng, South Africa"
```

### Example 4: Custom Output Directory

```bash
python3 scripts/astrology.py analyze "elon-musk" --output-dir ./my_charts
```

## Output

The skill generates the following outputs:

1. **Screenshot**: Full page screenshot of the natal chart (PNG format)
2. **OCR Text**: Extracted text from the screenshot
3. **Parsed Data**: Name, birth date, birth time, and location
4. **Graph Prompt**: Graph-based structural prompt for analysis
5. **Analysis**: Comprehensive astrological interpretation

## Dependencies

- **agent-browser**: Browser automation for navigation and screenshots
- **OCR**: Text extraction from images (tesseract or similar)
- **horoscope-fetcher**: Natal chart data fetching and analysis

## Notes

- **URL Format**: Celebrity names should be in URL slug format (lowercase, hyphens instead of spaces)
- **OCR Accuracy**: OCR accuracy may vary depending on image quality and font rendering
- **Manual Override**: Use `--skip-ocr` with manual data if OCR fails
- **Browser Mode**: Use `--headed` for debugging or visual verification
- **Timezone**: Birth time is assumed to be in local time; the script handles timezone conversion

## Supported Celebrities

The skill works with any celebrity available on astro-charts.com. Common examples include:

- elon-musk
- john-lennon
- oprah-winfrey
- steve-jobs
- albert-einstein
- marilyn-monroe

To find more celebrities, visit https://astro-charts.com/persons/

## Troubleshooting

### OCR Fails to Extract Data

If OCR fails to extract birth information:

1. Use `--headed` to visually verify the screenshot
2. Try manual data entry with `--skip-ocr`
3. Check screenshot quality in the output directory

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

## API Reference

### astro-charts.com

**Base URL**: `https://astro-charts.com/persons/chart/{name}/`

**Parameters**:
- `name`: Celebrity name in URL slug format

### horoscope-fetcher

See horoscope-fetcher skill documentation for detailed API reference.

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
