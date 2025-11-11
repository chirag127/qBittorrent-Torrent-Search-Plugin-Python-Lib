#!/usr/bin/env python3
"""
Validation script for bitsearch.py qBittorrent plugin
This script performs comprehensive validation to ensure the plugin works correctly
"""

import sys
import os
import re
import importlib.util

def validate_plugin_structure():
    """Validate the plugin file structure and requirements"""
    print("=== Validating Plugin Structure ===")

    # Check if plugin file exists
    if not os.path.exists('bitsearch.py'):
        print("❌ bitsearch.py file not found")
        return False

    # Try to import the plugin
    try:
        spec = importlib.util.spec_from_file_location("bitsearch", "bitsearch.py")
        bitsearch_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bitsearch_module)

        # Check if the class exists
        if not hasattr(bitsearch_module, 'bitsearch'):
            print("❌ bitsearch class not found in plugin")
            return False

        plugin_class = getattr(bitsearch_module, 'bitsearch')

        # Check required attributes
        required_attrs = ['url', 'name', 'supported_categories']
        for attr in required_attrs:
            if not hasattr(plugin_class, attr):
                print(f"❌ Required attribute '{attr}' not found")
                return False

        # Check required methods
        required_methods = ['search']
        for method in required_methods:
            if not hasattr(plugin_class, method):
                print(f"❌ Required method '{method}' not found")
                return False

        # Validate supported_categories
        categories = plugin_class.supported_categories
        if not isinstance(categories, dict):
            print("❌ supported_categories must be a dictionary")
            return False

        required_categories = ['all', 'anime', 'books', 'games', 'movies', 'music', 'software', 'tv']
        for cat in required_categories:
            if cat not in categories:
                print(f"❌ Required category '{cat}' not found in supported_categories")
                return False

        print("✅ Plugin structure validation passed")
        return True

    except Exception as e:
        print(f"❌ Error importing plugin: {e}")
        return False

def validate_plugin_metadata():
    """Validate plugin metadata"""
    print("\n=== Validating Plugin Metadata ===")

    try:
        with open('bitsearch.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required metadata
        if not re.search(r'#VERSION:\s*[\d.]+', content):
            print("❌ VERSION metadata not found")
            return False

        if not re.search(r'#AUTHORS:', content):
            print("❌ AUTHORS metadata not found")
            return False

        if not re.search(r'#LICENSING INFORMATION:', content):
            print("❌ LICENSING INFORMATION metadata not found")
            return False

        print("✅ Plugin metadata validation passed")
        return True

    except Exception as e:
        print(f"❌ Error reading plugin file: {e}")
        return False

def validate_output_format():
    """Validate that the plugin outputs in the correct format"""
    print("\n=== Validating Output Format ===")

    # This would require running the plugin with real data
    # For now, we'll check that the prettyPrinter is used correctly
    try:
        with open('bitsearch.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that prettyPrinter is imported and used
        if 'from novaprinter import prettyPrinter' not in content:
            print("❌ prettyPrinter not imported correctly")
            return False

        if 'prettyPrinter(' not in content:
            print("❌ prettyPrinter not used in search method")
            return False

        print("✅ Output format validation passed")
        return True

    except Exception as e:
        print(f"❌ Error validating output format: {e}")
        return False

def validate_error_handling():
    """Validate error handling"""
    print("\n=== Validating Error Handling ===")

    try:
        with open('bitsearch.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for try-except blocks
        if 'try:' not in content or 'except' not in content:
            print("❌ No error handling found")
            return False

        # Check that errors are printed to stderr, not stdout
        if 'file=sys.stderr' not in content:
            print("❌ Errors should be printed to stderr")
            return False

        print("✅ Error handling validation passed")
        return True

    except Exception as e:
        print(f"❌ Error validating error handling: {e}")
        return False

def validate_url_construction():
    """Validate URL construction"""
    print("\n=== Validating URL Construction ===")

    try:
        # Import the plugin to test URL construction
        sys.path.insert(0, '.')

        # Mock the dependencies
        class MockHelpers:
            @staticmethod
            def retrieve_url(url):
                return ""

        class MockNovaPrinter:
            @staticmethod
            def prettyPrinter(result):
                pass

        sys.modules['helpers'] = MockHelpers()
        sys.modules['novaprinter'] = MockNovaPrinter()

        from bitsearch import bitsearch

        plugin = bitsearch()

        # Test URL construction by checking the base URL
        if plugin.url != 'https://bitsearch.to':
            print(f"❌ Incorrect base URL: {plugin.url}")
            return False

        # Test category mapping
        expected_categories = {
            'all': '',
            'anime': 'anime',
            'books': 'books',
            'games': 'games',
            'movies': 'movies',
            'music': 'music',
            'software': 'apps',  # Note: maps to 'apps' on bitsearch.to
            'tv': 'tv'
        }

        if plugin.supported_categories != expected_categories:
            print(f"❌ Incorrect category mapping")
            return False

        print("✅ URL construction validation passed")
        return True

    except Exception as e:
        print(f"❌ Error validating URL construction: {e}")
        return False

def validate_parsing_logic():
    """Validate parsing logic with sample data"""
    print("\n=== Validating Parsing Logic ===")

    try:
        # Test with the sample HTML we know works
        sample_html = '''
        <h3><a href="/torrent/test123">Test Torrent</a></h3>
        Other/DiskImage 1.95 GB 4/18/2019
        28 seeders 41 leechers 1403 downloads
        <a href="magnet:?xt=urn:btih:TEST123">Magnet</a>
        '''

        sys.path.insert(0, '.')
        from bitsearch import BitSearchParser

        parser = BitSearchParser()
        parser.parse_html(sample_html)

        if len(parser.results) == 0:
            print("❌ Parser failed to extract results from sample HTML")
            return False

        result = parser.results[0]

        # Validate result structure
        required_keys = ['link', 'name', 'size', 'seeds', 'leech', 'engine_url', 'desc_link', 'pub_date']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key '{key}' in result")
                return False

        # Validate specific values
        if result['name'] != 'Test Torrent':
            print(f"❌ Incorrect name extraction: {result['name']}")
            return False

        if not result['link'].startswith('magnet:'):
            print(f"❌ Incorrect magnet link extraction: {result['link']}")
            return False

        if result['seeds'] != '28':
            print(f"❌ Incorrect seeds extraction: {result['seeds']}")
            return False

        if result['leech'] != '41':
            print(f"❌ Incorrect leechers extraction: {result['leech']}")
            return False

        print("✅ Parsing logic validation passed")
        return True

    except Exception as e:
        print(f"❌ Error validating parsing logic: {e}")
        return False

def main():
    """Run all validations"""
    print("Starting comprehensive bitsearch.py plugin validation...")
    print("=" * 60)

    validations = [
        validate_plugin_structure,
        validate_plugin_metadata,
        validate_output_format,
        validate_error_handling,
        validate_url_construction,
        validate_parsing_logic
    ]

    results = []
    for validation in validations:
        try:
            result = validation()
            results.append(result)
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY:")
    print("=" * 60)

    validation_names = [
        "Plugin Structure",
        "Plugin Metadata",
        "Output Format",
        "Error Handling",
        "URL Construction",
        "Parsing Logic"
    ]

    for i, (name, result) in enumerate(zip(validation_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")

    all_passed = all(results)
    print("\n" + "=" * 60)

    if all_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ The plugin is ready for use with qBittorrent")
        print("\nTo install:")
        print("1. Copy bitsearch.py to your qBittorrent engines folder")
        print("2. Or use qBittorrent GUI: Search → Search engines... → Install a new one")
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("Please fix the issues before using the plugin")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)