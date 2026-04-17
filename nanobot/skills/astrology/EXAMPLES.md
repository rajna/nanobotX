# Astrology Skill - Usage Examples

This document provides detailed examples of how to use the astrology skill.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Usage](#advanced-usage)
3. [Manual Data Entry](#manual-data-entry)
4. [Troubleshooting Examples](#troubleshooting-examples)

## Basic Usage

### Example 1: Analyze Elon Musk's Chart

```bash
python3 scripts/astrology.py analyze "elon-musk"
```

**What happens:**
1. Navigates to https://astro-charts.com/persons/chart/elon-musk/
2. Captures full page screenshot
3. Extracts text using OCR
4. Parses birth information
5. Generates graph-based structural prompt
6. Provides comprehensive analysis

**Output files:**
- `output/elon-musk_chart.png` - Screenshot of the natal chart
- `output/elon-musk_ocr.txt` - Extracted OCR text
- `output/elon-musk_parsed.json` - Parsed birth data
- `output/elon-musk_graph_prompt.txt` - Graph-based structural prompt
- `output/elon-musk_analysis.md` - Comprehensive analysis

### Example 2: Analyze John Lennon's Chart

```bash
python3 scripts/astrology.py analyze "john-lennon"
```

### Example 3: Analyze Oprah Winfrey's Chart

```bash
python3 scripts/astrology.py analyze "oprah-winfrey"
```

## Advanced Usage

### Example 4: Run with Headed Browser (Debugging)

```bash
python3 scripts/astrology.py analyze "elon-musk" --headed
```

**Use case:** When you want to see the browser in action for debugging or visual verification.

### Example 5: Custom Output Directory

```bash
python3 scripts/astrology.py analyze "elon-musk" --output-dir ./my_charts
```

**Use case:** When you want to organize output files in a specific directory.

### Example 6: Multiple Celebrities

```bash
# Create a batch script
for name in elon-musk john-lennon oprah-winfrey steve-jobs; do
    python3 scripts/astrology.py analyze "$name" --output-dir "./celebrity_charts"
done
```

## Manual Data Entry

### Example 7: Skip OCR and Use Manual Data

```bash
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, Gauteng, South Africa"
```

**Use case:** When OCR fails or you have accurate birth data from another source.

### Example 8: Manual Data with Coordinates

```bash
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --latitude -25.7479 \
  --longitude 28.2293
```

**Use case:** When you have precise coordinates instead of an address.

### Example 9: Manual Data for Historical Figures

```bash
python3 scripts/astrology.py analyze "albert-einstein" \
  --skip-ocr \
  --time "1879-03-14 11:30:00" \
  --address "Ulm, Germany"
```

**Use case:** For historical figures where OCR might not work well.

## Troubleshooting Examples

### Example 10: Debug OCR Issues

```bash
# Step 1: Run with headed browser to verify screenshot
python3 scripts/astrology.py analyze "elon-musk" --headed

# Step 2: Check the screenshot quality
open output/elon-musk_chart.png

# Step 3: Check OCR text
cat output/elon-musk_ocr.txt

# Step 4: If OCR fails, use manual data
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, South Africa"
```

### Example 11: Debug Browser Navigation

```bash
# Run with headed browser to see what's happening
python3 scripts/astrology.py analyze "unknown-celebrity" --headed

# Check if the URL is correct
# Visit https://astro-charts.com/persons/chart/unknown-celebrity/ manually
```

### Example 12: Debug Chart Generation

```bash
# Step 1: Check parsed data
cat output/elon-musk_parsed.json

# Step 2: Verify birth data is correct
# If not, use manual data
python3 scripts/astrology.py analyze "elon-musk" \
  --skip-ocr \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, South Africa"

# Step 3: Check if horoscope-fetcher is working
python3 ../horoscope-fetcher/scripts/horoscope_fetcher.py \
  gen_analyze_chart_graph_prompt \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, South Africa"
```

## Real-World Workflows

### Workflow 1: Research Project

```bash
# Create a research directory
mkdir -p ./research/tech_celebrities

# Analyze multiple tech celebrities
for name in elon-musk steve-jobs bill-gates mark-zuckerberg; do
    python3 scripts/astrology.py analyze "$name" \
      --output-dir "./research/tech_celebrities"
done

# Review all analyses
open ./research/tech_celebrities/*_analysis.md
```

### Workflow 2: Comparative Analysis

```bash
# Analyze two celebrities for comparison
python3 scripts/astrology.py analyze "elon-musk" --output-dir "./comparison"
python3 scripts/astrology.py analyze "steve-jobs" --output-dir "./comparison"

# Compare their charts
diff comparison/elon-musk_graph_prompt.txt comparison/steve-jobs_graph_prompt.txt
```

### Workflow 3: Batch Processing

```bash
# Create a list of celebrities
cat > celebrities.txt << EOF
elon-musk
john-lennon
oprah-winfrey
steve-jobs
albert-einstein
marilyn-monroe
EOF

# Process all celebrities
while read name; do
    echo "Processing $name..."
    python3 scripts/astrology.py analyze "$name" --output-dir "./batch_output"
done < celebrities.txt

# Generate summary
echo "Processed $(ls batch_output/*_analysis.md | wc -l) celebrities"
```

## Tips and Best Practices

1. **Use Headed Mode for Debugging**: When something goes wrong, run with `--headed` to see what's happening.

2. **Verify OCR Results**: Always check the OCR text file to ensure data was extracted correctly.

3. **Use Manual Data for Accuracy**: If you have accurate birth data from a reliable source, use `--skip-ocr` for better results.

4. **Organize Output**: Use `--output-dir` to organize output files by project or category.

5. **Check Parsed Data**: Review the parsed JSON file to ensure birth data was correctly extracted.

6. **Test with Known Data**: Before analyzing unknown celebrities, test with well-known ones to verify the workflow.

## Common Issues and Solutions

### Issue: OCR fails to extract birth date

**Solution:**
```bash
# Use manual data entry
python3 scripts/astrology.py analyze "celebrity-name" \
  --skip-ocr \
  --time "YYYY-MM-DD HH:MM:SS" \
  --address "City, Country"
```

### Issue: Browser navigation fails

**Solution:**
```bash
# Check if the URL is correct
# Visit https://astro-charts.com/persons/chart/celebrity-name/ manually

# Use headed mode to debug
python3 scripts/astrology.py analyze "celebrity-name" --headed
```

### Issue: Chart generation fails

**Solution:**
```bash
# Verify parsed data
cat output/celebrity-name_parsed.json

# Check horoscope-fetcher
python3 ../horoscope-fetcher/scripts/horoscope_fetcher.py \
  gen_analyze_chart_graph_prompt \
  --time "YYYY-MM-DD HH:MM:SS" \
  --address "City, Country"
```

## Additional Resources

- [astro-charts.com](https://astro-charts.com/) - Source of celebrity natal charts
- [horoscope-fetcher Skill](../horoscope-fetcher/SKILL.md) - Natal chart data fetching
- [agent-browser Skill](../agent-browser-0.2.0/SKILL.md) - Browser automation

## Support

For issues or questions, please refer to the main [README.md](README.md) or [SKILL.md](SKILL.md) files.
