#!/usr/bin/env python3
"""
Test script for bitsearch.py qBittorrent plugin
Usage: python test_bitsearch.py [search_term] [category]
"""

import sys
import os

# Add current directory to path so we can import the plugin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the required modules for testing
class MockHelpers:
    @staticmethod
    def retrieve_url(url):
        """Mock retrieve_url - in real usage this fetches web content"""
        print(f"Would fetch: {url}", file=sys.stderr)
        # Return empty string to simulate no content (for testing)
        return ""

    @staticmethod
    def download_file(info):
        """Mock download_file"""
        return f"/tmp/mock_torrent {info}"

class MockNovaPrinter:
    @staticmethod
    def prettyPrinter(result_dict):
        """Mock prettyPrinter - formats output for qBittorrent"""
        link = result_dict.get('link', '')
        name = result_dict.get('name', '')
        size = result_dict.get('size', '-1')
        seeds = result_dict.get('seeds', '-1')
        leech = result_dict.get('leech', '-1')
        engine_url = result_dict.get('engine_url', '')
        desc_link = result_dict.get('desc_link', '')
        pub_date = result_dict.get('pub_date', '-1')

        print(f"{link}|{name}|{size}|{seeds}|{leech}|{engine_url}|{desc_link}|{pub_date}")

# Replace the imports with our mocks
sys.modules['helpers'] = MockHelpers()
sys.modules['novaprinter'] = MockNovaPrinter()

# Now import the plugin
from bitsearch import bitsearch

def test_plugin():
    """Test the bitsearch plugin"""
    # Get command line arguments
    search_term = sys.argv[1] if len(sys.argv) > 1 else "ubuntu"
    category = sys.argv[2] if len(sys.argv) > 2 else "all"

    print(f"Testing bitsearch plugin with search term: '{search_term}', category: '{category}'", file=sys.stderr)
    print(f"Plugin URL: {bitsearch.url}", file=sys.stderr)
    print(f"Plugin Name: {bitsearch.name}", file=sys.stderr)
    print(f"Supported Categories: {bitsearch.supported_categories}", file=sys.stderr)
    print("", file=sys.stderr)

    # Create plugin instance
    plugin = bitsearch()

    # Test search
    print("Search results:", file=sys.stderr)
    plugin.search(search_term, category)

    print("", file=sys.stderr)
    print("Test completed. In real usage, results would be fetched from bitsearch.to", file=sys.stderr)

if __name__ == "__main__":
    test_plugin()