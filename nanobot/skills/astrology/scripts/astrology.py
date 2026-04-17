#!/usr/bin/env python3
"""
Astrology - Fetch and analyze celebrity natal charts from astro-charts.com
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "skills" / "horoscope-fetcher" / "scripts"))

try:
    import horoscope_fetcher
except ImportError:
    print("Warning: horoscope_fetcher module not found. Some features may not work.")
    horoscope_fetcher = None


class AstrologyAnalyzer:
    """Main class for analyzing celebrity natal charts"""

    def __init__(self, output_dir="./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def navigate_and_capture(self, name, headed=False):
        """
        Navigate to astro-charts.com and capture page content

        Args:
            name: Celebrity name (URL slug format)
            headed: Run browser in headed mode

        Returns:
            Extracted text content
        """
        url = f"https://astro-charts.com/persons/chart/{name}/"

        print(f"Navigating to: {url}")

        # Build agent-browser command
        cmd = ["agent-browser", "open", url]
        if headed:
            cmd.append("--headed")

        # Navigate to the page
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
            print("✓ Navigation successful")
        except subprocess.CalledProcessError as e:
            print(f"✗ Navigation failed: {e}")
            print(f"stderr: {e.stderr}")
            return None
        except subprocess.TimeoutExpired:
            print("✗ Navigation timed out")
            return None

        # Wait a bit for the page to load
        import time
        time.sleep(3)

        # Capture page content using snapshot
        print("Capturing page content...")
        try:
            result = subprocess.run(
                ["agent-browser", "snapshot"],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            text = result.stdout
            print(f"✓ Page content captured ({len(text)} characters)")
            return text
        except subprocess.CalledProcessError as e:
            print(f"✗ Snapshot failed: {e}")
            print(f"stderr: {e.stderr}")
            return None
        except subprocess.TimeoutExpired:
            print("✗ Snapshot timed out")
            return None

    def extract_text_with_ocr(self, image_path):
        """
        Extract text from image using OCR (deprecated - now using snapshot directly)

        Args:
            image_path: Path to image file

        Returns:
            Extracted text string
        """
        # This method is deprecated - we now use snapshot directly
        print("Warning: extract_text_with_ocr is deprecated. Using snapshot instead.")
        return ""

    def parse_birth_data(self, text, name):
        """
        Parse birth data from OCR text

        Args:
            text: OCR extracted text
            name: Celebrity name

        Returns:
            Dictionary with parsed data (name, birth_date, birth_time, location)
        """
        print("Parsing birth data from OCR text...")

        # Save OCR text for inspection
        ocr_text_path = self.output_dir / f"{name}_ocr.txt"
        with open(ocr_text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ OCR text saved to: {ocr_text_path}")

        # Try to extract birth date and time
        # Common patterns: "June 28, 1971 at 7:30 AM", "June 28, 1971 7:30 AM", "1971-06-28 07:30", etc.
        date_patterns = [
            r'(\w+\s+\d{1,2},?\s+\d{4})\s+at\s+(\d{1,2}:\d{2}\s*[AP]M)',  # June 28, 1971 at 7:30 AM
            r'(\w+\s+\d{1,2},?\s+\d{4})\s+(\d{1,2}:\d{2}\s*[AP]M)',  # June 28, 1971 7:30 AM
            r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})',  # 1971-06-28 07:30
            r'(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}:\d{2}\s*[AP]M)',  # 6/28/1971 7:30 AM
        ]

        birth_date = None
        birth_time = None
        location = None

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                birth_date = match.group(1)
                birth_time = match.group(2)
                print(f"✓ Found birth date: {birth_date}")
                print(f"✓ Found birth time: {birth_time}")
                break

        # Try to extract location
        location_patterns = [
            r'born\s+in\s+([A-Za-z\s,]+)',  # born in Pretoria, South Africa
            r'location:\s*([A-Za-z\s,]+)',  # location: Pretoria, South Africa
            r'([A-Z][a-z]+,\s*[A-Z][a-z]+,\s*[A-Z][a-z]+)',  # Pretoria, Gauteng, South Africa
            r'([A-Z][a-z]+,\s*[A-Z][a-z]+)',  # Pretoria, Gauteng
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                print(f"✓ Found location: {location}")
                break

        # Convert date format if needed
        if birth_date and birth_time:
            try:
                # Try to parse and standardize the date
                datetime_str = f"{birth_date} {birth_time}"
                # Try different formats
                for fmt in ["%B %d, %Y %I:%M %p", "%Y-%m-%d %H:%M", "%m/%d/%Y %I:%M %p"]:
                    try:
                        dt = datetime.strptime(datetime_str, fmt)
                        birth_date = dt.strftime("%Y-%m-%d")
                        birth_time = dt.strftime("%H:%M:%S")
                        print(f"✓ Standardized datetime: {birth_date} {birth_time}")
                        break
                    except ValueError:
                        continue
            except Exception as e:
                print(f"Warning: Could not standardize datetime: {e}")

        parsed_data = {
            "name": name.replace("-", " ").title(),
            "birth_date": birth_date,
            "birth_time": birth_time,
            "location": location
        }

        # Save parsed data
        parsed_data_path = self.output_dir / f"{name}_parsed.json"
        with open(parsed_data_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Parsed data saved to: {parsed_data_path}")

        return parsed_data

    def generate_chart_analysis(self, parsed_data, latitude=None, longitude=None, source_tz_offset=8):
        """
        Generate graph-based structural prompt for natal chart analysis

        Args:
            parsed_data: Dictionary with birth data
            latitude: Manual latitude
            longitude: Manual longitude
            source_tz_offset: Source timezone offset in hours

        Returns:
            Graph-based structural prompt string
        """
        if not horoscope_fetcher:
            print("✗ horoscope_fetcher not available. Cannot generate chart analysis.")
            return None

        name = parsed_data["name"].lower().replace(" ", "-")
        birth_date = parsed_data["birth_date"]
        birth_time = parsed_data["birth_time"]
        location = parsed_data["location"]

        if not birth_date or not birth_time:
            print("✗ Missing birth date or time. Cannot generate chart analysis.")
            return None

        print("Generating graph-based structural prompt...")

        # Build command for horoscope_fetcher
        cmd = [
            "python3",
            str(Path(__file__).parent.parent.parent.parent / "skills" / "horoscope-fetcher" / "scripts" / "horoscope_fetcher.py"),
            "gen_analyze_chart_graph_prompt",
            "--time", f"{birth_date} {birth_time}",
            "--source-tz-offset", str(source_tz_offset)
        ]

        if location:
            cmd.extend(["--address", location])

        if latitude is not None:
            cmd.extend(["--latitude", str(latitude)])

        if longitude is not None:
            cmd.extend(["--longitude", str(longitude)])

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            graph_prompt = result.stdout
            print(f"✓ Graph prompt generated ({len(graph_prompt)} characters)")

            # Save graph prompt
            graph_prompt_path = self.output_dir / f"{name}_graph_prompt.txt"
            with open(graph_prompt_path, 'w', encoding='utf-8') as f:
                f.write(graph_prompt)
            print(f"✓ Graph prompt saved to: {graph_prompt_path}")

            return graph_prompt
        except subprocess.CalledProcessError as e:
            print(f"✗ Graph prompt generation failed: {e}")
            print(f"stderr: {e.stderr}")
            return None

    def analyze_chart(self, graph_prompt, parsed_data):
        """
        Provide comprehensive astrological analysis based on graph prompt

        Args:
            graph_prompt: Graph-based structural prompt
            parsed_data: Dictionary with birth data

        Returns:
            Analysis text
        """
        print("Generating comprehensive astrological analysis...")

        name = parsed_data["name"]
        analysis = f"""
# Astrological Analysis for {name}

## Birth Information
- **Name**: {name}
- **Birth Date**: {parsed_data['birth_date']}
- **Birth Time**: {parsed_data['birth_time']}
- **Location**: {parsed_data['location']}

## Graph-Based Structural Analysis

{graph_prompt}

## Key Insights

Based on the natal chart structure above, here are the key astrological insights:

### Core Identity (Sun, Moon, Ascendant)
The Sun represents the core self and life purpose, the Moon represents emotional nature and inner needs, and the Ascendant represents the outer personality and first impressions. The interplay between these three points forms the foundation of the personality.

### Elemental Balance
The distribution of planets across the four elements (Fire, Earth, Air, Water) reveals the individual's natural strengths and challenges. A balanced distribution indicates versatility, while an emphasis on one element suggests specific talents and potential blind spots.

### Modal Balance
The distribution across the three modalities (Cardinal, Fixed, Mutable) indicates how the individual initiates action, maintains stability, and adapts to change.

### Planetary Aspects
The aspects between planets reveal the dynamic relationships within the psyche. Harmonious aspects (trines, sextiles) indicate natural talents and ease, while challenging aspects (squares, oppositions) indicate areas of growth and tension.

### House Placements
The houses show where planetary energies are expressed in life areas. The house placement of the Sun shows where the individual shines, while the Moon's house shows emotional needs.

### Retrograde Planets
Retrograde planets indicate internalized energy and karmic lessons. These areas often require extra attention and introspection.

---

*This analysis is based on the graph-based structural framework for natal chart interpretation. For a deeper understanding, consider consulting with a professional astrologer.*
"""

        # Save analysis
        name_slug = parsed_data["name"].lower().replace(" ", "-")
        analysis_path = self.output_dir / f"{name_slug}_analysis.md"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(analysis)
        print(f"✓ Analysis saved to: {analysis_path}")

        return analysis

    def run(self, name, headed=False, skip_ocr=False, manual_time=None, manual_address=None, manual_lat=None, manual_lon=None):
        """
        Run the complete analysis workflow

        Args:
            name: Celebrity name (URL slug format)
            headed: Run browser in headed mode
            skip_ocr: Skip OCR and use manual data
            manual_time: Manual birth time
            manual_address: Manual birth location
            manual_lat: Manual latitude
            manual_lon: Manual longitude
        """
        print(f"\n{'='*60}")
        print(f"Astrological Analysis for: {name}")
        print(f"{'='*60}\n")

        parsed_data = None

        if not skip_ocr:
            # Step 1: Navigate and capture page content
            text = self.navigate_and_capture(name, headed)
            if not text:
                print("✗ Failed to capture page content. Exiting.")
                return

            # Step 2: Parse birth data
            parsed_data = self.parse_birth_data(text, name)
        else:
            # Use manual data
            parsed_data = {
                "name": name.replace("-", " ").title(),
                "birth_date": manual_time.split()[0] if manual_time else None,
                "birth_time": manual_time.split()[1] if manual_time and len(manual_time.split()) > 1 else None,
                "location": manual_address
            }
            print(f"✓ Using manual data: {parsed_data}")

        # Step 4: Generate chart analysis
        # Determine source timezone offset based on location
        source_tz_offset = 8  # default CST
        if parsed_data.get("location"):
            loc_lower = parsed_data["location"].lower()
            if "south africa" in loc_lower or "pretoria" in loc_lower:
                source_tz_offset = 2
            elif "usa" in loc_lower or "united states" in loc_lower or "america" in loc_lower:
                source_tz_offset = -5  # EST default
            elif "uk" in loc_lower or "england" in loc_lower or "london" in loc_lower:
                source_tz_offset = 0
            elif "japan" in loc_lower or "tokyo" in loc_lower:
                source_tz_offset = 9

        graph_prompt = self.generate_chart_analysis(
            parsed_data,
            latitude=manual_lat,
            longitude=manual_lon,
            source_tz_offset=source_tz_offset
        )
        if not graph_prompt:
            print("✗ Failed to generate chart analysis. Exiting.")
            return

        # Step 5: Analyze chart
        analysis = self.analyze_chart(graph_prompt, parsed_data)

        print(f"\n{'='*60}")
        print("✓ Analysis Complete!")
        print(f"{'='*60}\n")
        print(analysis)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze celebrity natal charts from astro-charts.com"
    )
    parser.add_argument(
        "name",
        help="Celebrity name (URL slug format, e.g., 'elon-musk')"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Output directory for screenshots and results (default: ./output)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode"
    )
    parser.add_argument(
        "--skip-ocr",
        action="store_true",
        help="Skip OCR and use manual data entry"
    )
    parser.add_argument(
        "--time",
        help="Manual birth time (format: YYYY-MM-DD HH:MM:SS)"
    )
    parser.add_argument(
        "--address",
        help="Manual birth location"
    )
    parser.add_argument(
        "--latitude",
        type=float,
        help="Manual latitude"
    )
    parser.add_argument(
        "--longitude",
        type=float,
        help="Manual longitude"
    )

    args = parser.parse_args()

    analyzer = AstrologyAnalyzer(output_dir=args.output_dir)
    analyzer.run(
        name=args.name,
        headed=args.headed,
        skip_ocr=args.skip_ocr,
        manual_time=args.time,
        manual_address=args.address,
        manual_lat=args.latitude,
        manual_lon=args.longitude
    )


if __name__ == "__main__":
    main()
