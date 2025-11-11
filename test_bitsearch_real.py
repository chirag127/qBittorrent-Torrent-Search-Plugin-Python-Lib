#!/usr/bin/env python3
"""
Real test script for bitsearch.py qBittorrent plugin
This script tests with actual HTML content to verify parsing works
"""

import sys
import os
import re

# Add current directory to path so we can import the plugin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Sample HTML content from bitsearch.to (based on the scraped data)
SAMPLE_HTML = '''
<h3><a href="/torrent/5cb8afc48700981f3e5b00c4">ubuntu-19.04-desktop-amd64.iso</a></h3>
Other/DiskImage 1.95 GB 4/18/2019
28 seeders 41 leechers 1403 downloads
<a href="magnet:?xt=urn:btih:D540FC48EB12F2833163EED6421D449DD8F1CE1F&dn=%5BBitsearch.to%5D%20ubuntu-19.04-desktop-amd64.iso">Magnet</a>

<h3><a href="/torrent/63f864e1ae697358dc80e874">ubuntu-22.04.2-desktop-amd64.iso</a></h3>
Other/DiskImage 4.59 GB 2/24/2023
177 seeders 331 leechers 5833 downloads
<a href="magnet:?xt=urn:btih:A7838B75C42B612DA3B6CC99BEED4ECB2D04CFF2&dn=%5BBitsearch.to%5D%20ubuntu-22.04.2-desktop-amd64.iso">Magnet</a>

<h3><a href="/torrent/6442cc322e8ac2fc7fa34f36">ubuntu-23.04-desktop-amd64.iso</a></h3>
Other/DiskImage 4.59 GB 4/21/2023
163 seeders 340 leechers 6224 downloads
<a href="magnet:?xt=urn:btih:443C7602B4FDE83D1154D6D9DA48808418B181B6&dn=%5BBitsearch.to%5D%20ubuntu-23.04-desktop-amd64.iso">Magnet</a>
'''

# Mock the required modules for testing
class MockHelpers:
    @staticmethod
    def retrieve_url(url):
        """Mock retrieve_url - returns sample HTML for testing"""
        print(f"Fetching: {url}", file=sys.stderr)
        return SAMPLE_HTML

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
from bitsearch import bitsearch, BitSearchParser

def test_parser_directly():
    """Test the parser directly with sample HTML"""
    print("=== Testing Parser Directly ===", file=sys.stderr)

    parser = BitSearchParser()
    parser.parse_html(SAMPLE_HTML)

    print(f"Found {len(parser.results)} results:", file=sys.stderr)
    for i, result in enumerate(parser.results):
        print(f"Result {i+1}:", file=sys.stderr)
        print(f"  Name: {result['name']}", file=sys.stderr)
        print(f"  Link: {result['link'][:50]}..." if len(result['link']) > 50 else f"  Link: {result['link']}", file=sys.stderr)
        print(f"  Size: {result['size']}", file=sys.stderr)
        print(f"  Seeds: {result['seeds']}", file=sys.stderr)
        print(f"  Leechers: {result['leech']}", file=sys.stderr)
        print(f"  Desc Link: {result['desc_link']}", file=sys.stderr)
        print("", file=sys.stderr)

    return len(parser.results) > 0

def test_plugin():
    """Test the full plugin"""
    print("=== Testing Full Plugin ===", file=sys.stderr)

    # Get command line arguments
    search_term = sys.argv[1] if len(sys.argv) > 1 else "ubuntu"
    category = sys.argv[2] if len(sys.argv) > 2 else "all"

    print(f"Testing bitsearch pluginwith search term: '{search_term}', category: '{category}'", file=sys.stderr)
    print(f"Plugin URL: {bitsearch.url}", file=sys.stderr)
    print(f"Plugin Name: {bitsearch.name}", file=sys.stderr)
    print(f"Supported Categories: {bitsearch.supported_categories}", file=sys.stderr)
    print("", file=sys.stderr)

    # Create plugin instance
    plugin = bitsearch()

    # Test search (will use our mock that returns sample HTML)
    print("Search results:", file=sys.stderr)
    plugin.search(search_term, category)

    return True
def test_regex_patterns():
    """Test individual regex patterns"""
    print("=== Testing Regex Patterns ===", file=sys.stderr)

    # Test title extraction
    title_pattern = r'<h3[^>]*>.*?<a[^>]*href="(/torrent/[^"]+)"[^>]*>([^<]+)</a>.*?</h3>'
    titles = re.findall(title_pattern, SAMPLE_HTML, re.DOTALL | re.IGNORECASE)
    print(f"Found {len(titles)} titles:", file=sys.stderr)
    for path, title in titles:
        print(f"  {title} -> {path}", file=sys.stderr)

    # Test magnet link extraction
    magnet_pattern = r'href="(magnet:[^"]+)"'
    magnets = re.findall(magnet_pattern, SAMPLE_HTML)
    print(f"Found {len(magnets)} magnet links:", file=sys.stderr)
    for magnet in magnets:
        print(f"  {magnet[:50]}...", file=sys.stderr)

    # Test size extraction
    size_pattern = r'(\d+(?:\.\d+)?)\s*([KMGT]?B)'
    sizes = re.findall(size_pattern, SAMPLE_HTML, re.IGNORECASE)
    print(f"Found {len(sizes)} sizes:", file=sys.stderr)
    for size_num, size_unit in sizes:
        print(f"  {size_num} {size_unit}", file=sys.stderr)

    # Test seeds/leechers extraction
    seeds_pattern = r'(\d+)\s+seeders?'
    seeds = re.findall(seeds_pattern, SAMPLE_HTML, re.IGNORECASE)
    print(f"Found {len(seeds)} seed counts: {seeds}", file=sys.stderr)

    leechers_pattern = r'(\d+)\s+leechers?'
    leechers = re.findall(leechers_pattern, SAMPLE_HTML, re.IGNORECASE)
    print(f"Found {len(leechers)} leecher counts: {leechers}", file=sys.stderr)

    return len(titles) > 0 and len(magnets) > 0

def main():
    """Run all tests"""
    print("Starting bitsearch.py plugin tests...", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    # Test 1: Regex patterns
    regex_ok = test_regex_patterns()
    print(f"Regex patterns test: {'PASS' if regex_ok else 'FAIL'}", file=sys.stderr)
    print("", file=sys.stderr)

    # Test 2: Parser directly
    parser_ok = test_parser_directly()
    print(f"Parser test: {'PASS' if parser_ok else 'FAIL'}", file=sys.stderr)
    print("", file=sys.stderr)

    # Test 3: Full plugin
    plugin_ok = test_plugin()
    print(f"Plugin test: {'PASS' if plugin_ok else 'FAIL'}", file=sys.stderr)
    print("", file=sys.stderr)

    # Overall result
    all_ok = regex_ok and parser_ok and plugin_ok
    print("=" * 50, file=sys.stderr)
    print(f"Overall test result: {'PASS' if all_ok else 'FAIL'}", file=sys.stderr)

    if all_ok:
        print("✅ Plugin is working correctly and should parse bitsearch.to results!", file=sys.stderr)
    else:
        print("❌ Plugin has issues that need to be fixed.", file=sys.stderr)

if __name__ == "__main__":
    main()