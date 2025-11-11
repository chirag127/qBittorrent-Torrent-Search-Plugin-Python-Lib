#VERSION: 1.00
#AUTHORS: Kiro AI Assistant
#LICENSING INFORMATION: Public Domain

from html.parser import HTMLParser
from helpers import retrieve_url, download_file
from novaprinter import prettyPrinter
import re
import urllib.parse


class bitsearch(object):
    """
    BitSearch.to search engine plugin for qBittorrent
    """

    url = 'https://bitsearch.to'
    name = 'BitSearch'
    supported_categories = {
        'all': '',
        'anime': 'anime',
        'books': 'books',
        'games': 'games',
        'movies': 'movies',
        'music': 'music',
        'software': 'apps',
        'tv': 'tv'
    }

    def __init__(self):
        pass

    def download_torrent(self, info):
        """Download torrent file"""
        print(download_file(info))

    def search(self, what, cat='all'):
        """
        Search for torrents on bitsearch.to
        """
        # URL encode the search query
        query = urllib.parse.quote_plus(what)

        # Build search URL
        if cat == 'all':
            search_url = f"{self.url}/search?q={query}"
        else:
            category = self.supported_categories.get(cat, '')
            if category:
                search_url = f"{self.url}/search?q={query}&category={category}"
            else:
                search_url = f"{self.url}/search?q={query}"

        # Search multiple pages for better results
        for page in range(1, 4):  # Search first 3 pages
            if page > 1:
                page_url = f"{search_url}&page={page}"
            else:
                page_url = search_url

            try:
                # Get page content
                html_content = retrieve_url(page_url)
                if not html_content:
                    continue

                # Parse the HTML content
                parser = BitSearchParser()
                parser.parse_html(html_content)

                # Process results
                for result in parser.results:
                    # Validate result has required fields
                    if result.get('name') and result.get('link'):
                        prettyPrinter(result)

            except Exception as e:
                # Don't print to stdout, use stderr for errors
                import sys
                print(f"Error searching page {page}: {str(e)}", file=sys.stderr)
                continue


class BitSearchParser:
    """
    HTML parser for bitsearch.to search results
    Based on actual website structure analysis
    """

    def __init__(self):
        self.results = []

    def parse_html(self, html_content):
        """Parse search results using regex patterns based on actual site structure"""
        try:
            # Clean up HTML content
            html_content = html_content.replace('\n', ' ').replace('\r', ' ')

            # Extract torrent results based on actual bitsearch.to structure
            self.extract_bitsearch_results(html_content)

        except Exception as e:
            import sys
            print(f"Error in HTML parsing: {str(e)}", file=sys.stderr)

    def extract_bitsearch_results(self, html_content):
        """Extract results from bitsearch.to specific HTML structure"""

        # Pattern to match each torrent result block
        # Based on the actual structure: h3 with title link, followed by stats and magnet/torrent links
        result_pattern = r'<h3[^>]*>.*?<a[^>]*href="(/torrent/[^"]+)"[^>]*>([^<]+)</a>.*?</h3>(.*?)(?=<h3|<div[^>]*class="[^"]*pagination|$)'

        matches = re.findall(result_pattern, html_content, re.DOTALL | re.IGNORECASE)

        for match in matches:
            desc_link_path, title, content_block = match

            result = {
                'link': '',
                'name': title.strip(),
                'size': '-1',
                'seeds': '-1',
                'leech': '-1',
                'engine_url': 'https://bitsearch.to',
                'desc_link': 'https://bitsearch.to' + desc_link_path,
                'pub_date': '-1'
            }

            # Extract magnet link from the content block
            magnet_match = re.search(r'href="(magnet:[^"]+)"', content_block)
            if magnet_match:
                result['link'] = magnet_match.group(1)

            # Extract file size - look for patterns like "1.95 GB", "4.59 GB"
            size_match = re.search(r'(\d+(?:\.\d+)?)\s*([KMGT]?B)', content_block, re.IGNORECASE)
            if size_match:
                size_str = f"{size_match.group(1)} {size_match.group(2)}"
                size_bytes = self.parse_size(size_str)
                if size_bytes > 0:
                    result['size'] = str(size_bytes)

            # Extract seeds and leechers - look for patterns like "28 seeders 41 leechers"
            seeds_match = re.search(r'(\d+)\s+seeders?', content_block, re.IGNORECASE)
            if seeds_match:
                result['seeds'] = seeds_match.group(1)

            leechers_match = re.search(r'(\d+)\s+leechers?', content_block, re.IGNORECASE)
            if leechers_match:
                result['leech'] = leechers_match.group(1)

            # Extract date - look for date patterns like "4/18/2019"
            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', content_block)
            if date_match:
                timestamp = self.parse_date(date_match.group(1))
                if timestamp > 0:
                    result['pub_date'] = str(timestamp)

            # Only add if we have essential data
            if result['name'] and result['link']:
                self.results.append(result)

        # If the main pattern didn't work, try fallback extraction
        if not self.results:
            self.extract_fallback_results(html_content)

    def extract_fallback_results(self, html_content):
        """Fallback method to extract results if main pattern fails"""

        # Find all magnet links
        magnet_pattern = r'href="(magnet:[^"]+)"'
        magnets = re.findall(magnet_pattern, html_content)

        # Find all torrent titles (look for links to /torrent/ pages)
        title_pattern = r'<a[^>]*href="/torrent/[^"]*"[^>]*>([^<]+)</a>'
        titles = re.findall(title_pattern, html_content, re.IGNORECASE)

        # Find all file sizes
        size_pattern = r'(\d+(?:\.\d+)?)\s*([KMGT]?B)'
        sizes = re.findall(size_pattern, html_content, re.IGNORECASE)

        # Find seeds and leechers
        seeds_pattern = r'(\d+)\s+seeders?'
        seeds = re.findall(seeds_pattern, html_content, re.IGNORECASE)

        leechers_pattern = r'(\d+)\s+leechers?'
        leechers = re.findall(leechers_pattern, html_content, re.IGNORECASE)

        # Find description links
        desc_pattern = r'href="(/torrent/[^"]+)"'
        desc_links = re.findall(desc_pattern, html_content)

        # Combine results (match by index, assuming they appear in the same order)
        max_results = min(len(magnets), len(titles)) if titles else len(magnets)

        for i in range(max_results):
            result = {
                'link': magnets[i] if i < len(magnets) else '',
                'name': titles[i].strip() if i < len(titles) else f'Torrent {i+1}',
                'size': str(self.parse_size(f"{sizes[i][0]} {sizes[i][1]}")) if i < len(sizes) else '-1',
                'seeds': seeds[i] if i < len(seeds) else '-1',
                'leech': leechers[i] if i < len(leechers) else '-1',
                'engine_url': 'https://bitsearch.to',
                'desc_link': f'https://bitsearch.to{desc_links[i]}' if i < len(desc_links) else '',
                'pub_date': '-1'
            }

            # Only add if we have essential data
            if result['name'] and result['link']:
                self.results.append(result)

    def parse_size(self, size_str):
        """Convert size string to bytes"""
        try:
            size_str = size_str.upper().replace(',', '').strip()

            # Extract number and unit
            match = re.search(r'([\d.]+)\s*([KMGT]?B)', size_str)
            if not match:
                return -1

            number = float(match.group(1))
            unit = match.group(2)

            # Convert to bytes
            multipliers = {
                'B': 1,
                'KB': 1024,
                'MB': 1024**2,
                'GB': 1024**3,
                'TB': 1024**4
            }

            return int(number * multipliers.get(unit, 1))

        except:
            return -1

    def parse_date(self, date_str):
        """Parse date string to unix timestamp"""
        try:
            import time
            from datetime import datetime

            # Handle MM/DD/YYYY format (common on bitsearch.to)
            date_str = date_str.strip()

            # Try MM/DD/YYYY format first
            try:
                dt = datetime.strptime(date_str, '%m/%d/%Y')
                return int(time.mktime(dt.timetuple()))
            except:
                pass

            # Try other common formats
            patterns = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%Y-%m-%d %H:%M:%S',
                '%m/%d/%Y %H:%M:%S'
            ]

            for pattern in patterns:
                try:
                    dt = datetime.strptime(date_str, pattern)
                    return int(time.mktime(dt.timetuple()))
                except:
                    continue

            return -1

        except:
            return -1