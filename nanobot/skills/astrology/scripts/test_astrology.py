#!/usr/bin/env python3
"""
Test script for astrology skill
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from astrology import AstrologyAnalyzer


def test_basic_functionality():
    """Test basic functionality of astrology analyzer"""
    print("Testing Astrology Analyzer...\n")

    # Create analyzer with test output directory
    analyzer = AstrologyAnalyzer(output_dir="./test_output")

    # Test 1: Parse birth data from sample text
    print("Test 1: Parsing birth data from sample text")
    sample_text = """
    Elon Musk
    Born: June 28, 1971 7:30 AM
    Location: Pretoria, South Africa
    """

    parsed_data = analyzer.parse_birth_data(sample_text, "elon-musk")
    print(f"Parsed data: {parsed_data}")
    assert parsed_data["name"] == "Elon Musk"
    assert parsed_data["birth_date"] == "1971-06-28"
    assert parsed_data["birth_time"] == "07:30:00"
    assert parsed_data["location"] == "Pretoria, South Africa"
    print("✓ Test 1 passed\n")

    # Test 2: Parse birth data with different format
    print("Test 2: Parsing birth data with different format")
    sample_text2 = """
    John Lennon
    Born: 1940-10-09 17:30
    Location: Liverpool, UK
    """

    parsed_data2 = analyzer.parse_birth_data(sample_text2, "john-lennon")
    print(f"Parsed data: {parsed_data2}")
    assert parsed_data2["name"] == "John Lennon"
    assert parsed_data2["birth_date"] == "1940-10-09"
    assert parsed_data2["birth_time"] == "17:30:00"
    print("✓ Test 2 passed\n")

    print("All tests passed! ✓")


if __name__ == "__main__":
    test_basic_functionality()
