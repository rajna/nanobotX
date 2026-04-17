---
name: horoscope-fetcher
description: Fetch natal chart (birth chart) data from horoscope API. Use when the user needs to (1) Get natal chart data for a specific birth time and location, (2) Analyze planetary positions, aspects, and house placements, (3) Understand astrological chart interpretations, or (4) Get detailed horoscope information including zodiac signs, elements, and planetary aspects.
---

# Horoscope Fetcher

Fetch natal chart (birth chart) data from the deepastro.cn API.

## Features

- **Natal Chart Data**: Get complete birth chart information including planetary positions, aspects, and house placements
- **Automatic Geocoding**: Convert address to latitude/longitude automatically
- **Flexible Input**: Support various time formats and location inputs
- **Detailed Analysis**: Get comprehensive astrological interpretations
- **Analysis Prompt Generation**: Generate detailed prompts for LLM-based deep astrological analysis with graph-based framework
- **Graph Structure Generation**: Generate graph-based structural prompts for analyzing natal charts using node-edge relationships

## Usage

### Basic Usage

```bash
# Get natal chart with time and address
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --address "利物浦"

# Get natal chart with time and coordinates
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --latitude 53.41666 \
  --longitude -3

# Get natal chart with timezone
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --timezone "GMT" \
  --address "利物浦"
```

### Parameters

#### get_chart Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--time` | string | Yes | Birth time (format: YYYY-MM-DD HH:MM:SS) |
| `--address` | string | No* | Birth location (city name) |
| `--latitude` | float | No* | Latitude (decimal degrees) |
| `--longitude` | float | No* | Longitude (decimal degrees) |
| `--timezone` | string | No | Timezone (default: GMT) |
| `--show-desc` | flag | No | Show detailed descriptions (default: true) |
| `--no-show-desc` | flag | No | Hide detailed descriptions |
| `--json` | flag | No | Output in JSON format |

#### analyze_chart Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--time` | string | Yes | Birth time (format: YYYY-MM-DD HH:MM:SS) |
| `--address` | string | No* | Birth location (city name) |
| `--latitude` | float | No* | Latitude (decimal degrees) |
| `--longitude` | float | No* | Longitude (decimal degrees) |
| `--timezone` | string | No | Timezone (default: GMT) |
| `--model` | string | No | LLM model to use (default: gpt-4o-mini) |

#### gen_analyze_chart_graph_prompt Command

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--time` | string | Yes | Birth time (format: YYYY-MM-DD HH:MM:SS) |
| `--address` | string | No* | Birth location (city name) |
| `--latitude` | float | No* | Latitude (decimal degrees) |
| `--longitude` | float | No* | Longitude (decimal degrees) |
| `--timezone` | string | No | Timezone (default: GMT) |

**Note**: The `gen_analyze_chart_graph_prompt` command generates a graph-based structural prompt for analyzing natal charts. This prompt uses a node-edge framework where nodes represent astrological elements (planets, signs, houses, aspects, retrogrades) and edges represent relationships (harmony/challenge of aspects, sign traits, planetary characteristics, sign-planet correspondences).

* Either `--address` or `--latitude/--longitude` must be provided

### Output Format

The API returns comprehensive natal chart data:

```json
{
  "data": {
    "astros": {
      "sun": { "position": {...}, "sign": 7 },
      "moon": { "position": {...}, "sign": 11 },
      "mercury": { "position": {...}, "sign": 8 },
      ...
    },
    "axes": {
      "asc": { "position": {...}, "sign": 1 },
      "dc": { "position": {...}, "sign": 7 },
      "mc": { "position": {...}, "sign": 10 },
      "ic": { "position": {...}, "sign": 4 }
    },
    "houses": [...],
    "pairs": [...],
    "info1": "...",
    "info2": "...",
    "alldesc": "..."
  }
}
```

## Examples

### Example 1: Get John Lennon's Birth Chart

```bash
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1940-10-09 17:30:00" \
  --address "利物浦"
```

### Example 2: Get Chart with Coordinates

```bash
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074
```

### Example 3: Get Chart with Specific Timezone

```bash
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1985-06-15 08:30:00" \
  --timezone "CST" \
  --address "北京"
```

### Example 4: Get Chart without Detailed Descriptions

```bash
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074 \
  --no-show-desc
```

### Example 5: Get Chart in JSON Format

```bash
python3 scripts/horoscope_fetcher.py get_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074 \
  --json
```

### Example 6: Generate Analysis Prompt

```bash
# Generate analysis prompt for natal chart
python3 scripts/horoscope_fetcher.py analyze_chart \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074

# Use specific model (for reference only)
python3 scripts/horoscope_fetcher.py analyze_chart \
  --time "1990-01-01 12:00:00" \
  --address "北京" \
  --model "gpt-4o"
```

**Note**: The `analyze_chart` command generates a detailed analysis prompt based on the natal chart data. You can use this prompt with any LLM to get a deep astrological interpretation.

### Example 7: Generate Graph Structure Prompt

```bash
# Generate graph-based structural prompt for natal chart analysis
python3 scripts/horoscope_fetcher.py gen_analyze_chart_graph_prompt \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 \
  --longitude 116.4074

# Generate graph structure prompt with address
python3 scripts/horoscope_fetcher.py gen_analyze_chart_graph_prompt \
  --time "1971-06-28 07:30:00" \
  --address "Pretoria, Gauteng, South Africa" \
  --source-tz-offset 2
```

**Note**: The `gen_analyze_chart_graph_prompt` command generates a graph-based structural prompt that uses a node-edge framework for analyzing natal charts. This approach allows for:
- **Nodes**: Represent astrological elements (planets, signs, houses, aspects, retrogrades)
- **Edges**: Represent relationships (harmony/challenge of aspects, sign traits, planetary characteristics, sign-planet correspondences)
- **Graph Traversal**: Enables systematic analysis from core elements (Sun, Moon, Ascendant) to extended features (houses, planetary groups, key single planets)

This graph-based approach provides a structured framework for deep astrological interpretation, making it easier to identify patterns, relationships, and themes within the natal chart.

## Data Interpretation

### Zodiac Signs (0-11)

| Index | Sign | Chinese |
|-------|------|---------|
| 0 | Aries | 白羊 |
| 1 | Taurus | 金牛 |
| 2 | Gemini | 双子 |
| 3 | Cancer | 巨蟹 |
| 4 | Leo | 狮子 |
| 5 | Virgo | 处女 |
| 6 | Libra | 天秤 |
| 7 | Scorpio | 天蝎 |
| 8 | Sagittarius | 射手 |
| 9 | Capricorn | 摩羯 |
| 10 | Aquarius | 水瓶 |
| 11 | Pisces | 双鱼 |

### Aspect Types

| Type | Degrees | Name |
|------|---------|------|
| 0 | 0 | 合相 (Conjunction) |
| 60 | 60 | 六合 (Sextile) |
| 90 | 90 | 刑 (Square) |
| 120 | 120 | 拱 (Trine) |
| 180 | 180 | 冲 (Opposition) |

## Notes

- **Time Format**: Input time should be in local time. Use `--source-tz-offset` to specify the timezone offset (e.g., 8 for China/CST, 2 for South Africa/SAST, 0 for UK/GMT, -5 for US Eastern/EST). The script automatically converts to GMT (UTC) by subtracting the specified offset.
- **Default Behavior**: Detailed descriptions (`alldesc`) are shown by default. Use `--no-show-desc` to hide them.
- **URL Display**: The API URL is printed before fetching data for debugging purposes.
- **Address Geocoding**: Automatic if coordinates are not provided (uses OpenStreetMap Nominatim API).
- **Chart Data**: Includes all major planets, asteroids, and points.
- **Retrograde Planets**: Listed in `returninfo` field.
- **Sign Indexing**: API uses 1-based indexing for zodiac signs (not 0-based).
- **Graph Structure**: The `gen_analyze_chart_graph_prompt` command generates a structured prompt using a node-edge framework, enabling systematic analysis of natal charts through graph traversal.

## API Reference

**Base URL**: `https://horoscope.deepastro.cn/horoscope`

**Parameters**:
- `time`: Formatted time string (e.g., "Wed, 09 Oct 1940 17:30:00 GMT")
- `address`: Location name (URL encoded)
- `latitude`: Latitude in decimal degrees
- `longitude`: Longitude in decimal degrees
- `isShowDesc`: Show descriptions (true/false)

## JavaScript API (questionUtils.js) — DELETED

JS files (`comparisonData.js`, `questionUtils.js`) were deleted on 2026-03-16. All logic has been ported to Python. See CLI commands below for equivalent functionality.

## Python CLI Commands

### transit Command

获取行运盘信息（本命盘 vs 当前行运盘）。

```bash
python3 scripts/horoscope_fetcher.py transit \
  --time "2026-03-09 21:57:00" \
  --latitude 31.57 --longitude 120.30 \
  --source-tz-offset 8
```

**输出格式**: `行运信息:行运太阳,行运金星落5宫;太阳六合7宫天王星;...`

### compare Command

获取比较盘信息（两人星盘对比）。

```bash
python3 scripts/horoscope_fetcher.py compare \
  --time "1990-01-01 12:00:00" \
  --latitude 39.9042 --longitude 116.4074 \
  --source-tz-offset 8
```

### Python API (Module Functions)

```python
from horoscope_fetcher import get_horoscope, transit_desc, star_point_comparison

# 获取星盘数据
chart = get_horoscope(time_str, latitude, longitude, source_tz_offset, target_tz, show_desc)

# 行运描述
desc = transit_desc(time_str, latitude, longitude, source_tz_offset)

# 星盘比较 (chartType: 3=比较盘, 4=行运盘, 7=太阳弧)
result = star_point_comparison(chart1, chart2, chart_type=4)
print(result['desc'])
```

**IMPORTANT**: Module exports functions, NOT a class. `HoroscopeFetcher` class does not exist.

## Changelog

### Version 1.5.0 (2026-03-17)
- 🔴 **CRITICAL FIX**: `_get_star_longitude()` was returning sign-internal degrees (0°~30°) instead of ecliptic longitude (0°~360°). Added `(sign - 1) * 30` offset. This bug caused ALL house placements and aspects to be incorrect.
- ✅ Added `transit` CLI subcommand — fetch transit chart comparison
- ✅ Added `compare` CLI subcommand — fetch synastry chart comparison
- ✅ Reduced conjunction orb from 10° to 3° for transit analysis
- ✅ Excluded self-conjunctions from output
- ✅ Added aspect deduplication (best aspect per planet pair)
- ✅ Removed JS files (`comparisonData.js`, `questionUtils.js`) — fully ported to Python
- ✅ Updated SKILL.md with Python API docs, removed JS references

### Version 1.4.0 (2026-03-16)
- ✅ Added `transit_desc` method to `questionUtils.js` — automatically fetches natal chart + current transit chart and returns transit comparison description
- ✅ Added `getHoroscope` JS function — Node.js version of the horoscope API client (geocoding + time conversion + API call)
- ✅ Added `starPointComparison` export — compare two charts (natal vs transit, synastry, etc.)
- ✅ Fixed `comparisonHouse` undefined bug in `comparisonData.js`

### Version 1.3.0 (2026-03-13)
- ✅ Added `gen_analyze_chart_graph_prompt` command for generating graph-based structural prompts
- ✅ Implemented node-edge framework for natal chart analysis
- ✅ Added timezone offset support (`--source-tz-offset`) for accurate time conversion
- ✅ Updated documentation with graph structure generation examples
- ✅ Enhanced prompt generation with case study examples

### Version 1.2.0 (2026-03-13)
- ✅ Added `analyze_chart` command for generating analysis prompts
- ✅ Implemented graph-based analysis framework
- ✅ Added detailed prompt generation for LLM-based astrological interpretation
- ✅ Added `--model` parameter for reference (prompt includes model info)
- ✅ Updated documentation with analysis examples

### Version 1.1.0 (2026-03-13)
- ✅ Fixed `isShowDesc` default value to `true`
- ✅ Added `--show-desc` and `--no-show-desc` flags for controlling description display
- ✅ Added URL printing for debugging purposes
- ✅ Updated `print_summary()` function to support `show_desc` parameter
- ✅ **Fixed time conversion**: Now correctly converts local time (CST) to GMT by subtracting 8 hours

### Version 1.0.0
- Initial release
- Basic natal chart fetching functionality
- Automatic geocoding support
- JSON and summary output formats
