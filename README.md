# BitSearch.to qBittorrent Search Plugin

A qBittorrent search engine plugin for [bitsearch.to](https://bitsearch.to/), a popular torrent search engine.

## Features

- Search torrents on bitsearch.to
- Support for multiple categories (all, anime, books, games, movies, music, software, tv)
- Multi-page search results (searches first 3 pages)
- Extracts magnet links, torrent names, file sizes, seeds, and leechers
- Robust HTML parsing with fallback methods

## Installation

### Method 1: Through qBittorrent GUI

1. Download the `bitsearch.py` file
2. Open qBittorrent
3. Go to the Search tab
4. Click "Search engines..." button
5. Click "Install a new one" at the bottom
6. Select the `bitsearch.py` file
7. The plugin should now appear in your search engines list

### Method 2: Manual Installation

1. Download the `bitsearch.py` file
2. Copy it to your qBittorrent search engines directory:
   - **Windows**: `%LOCALAPPDATA%\qBittorrent\nova3\engines\`
   - **Linux**: `~/.local/share/qBittorrent/nova3/engines/`
   - **macOS**: `~/Library/Application Support/qBittorrent/nova3/engines/`
3. Restart qBittorrent

## Supported Categories

- **all**: Search all categories
- **anime**: Anime torrents
- **books**: Books and ebooks
- **games**: Video games
- **movies**: Movies
- **music**: Music and audio
- **software**: Software and applications (mapped to 'apps' on bitsearch.to)
- **tv**: TV shows and series

## Testing

You can test the plugin before installation using the included test script:

```bash
python test_bitsearch.py "ubuntu linux" all
```

This will show you the search URLs that would be generated and test the plugin structure.

## Technical Details

### Plugin Structure

The plugin follows the qBittorrent search plugin specification:

- **Class name**: `bitsearch` (must match filename without .py)
- **Required attributes**: `url`, `name`, `supported_categories`
- **Required methods**: `search(what, cat='all')`
- **Optional methods**: `download_torrent(info)`

### Search URL Format

The plugin constructs search URLs in the following format:
- Base search: `https://bitsearch.to/search?q={query}`
- With category: `https://bitsearch.to/search?q={query}&category={category}`
- With pagination: `https://bitsearch.to/search?q={query}&page={page}`

### HTML Parsing

The plugin uses a robust parsing approach:

1. **Structured parsing**: Looks for common HTML container patterns (div, tr, li, article)
2. **Regex-based extraction**: Uses regular expressions to extract torrent data
3. **Fallback method**: If structured parsing fails, falls back to individual component extraction
4. **Data validation**: Ensures extracted data meets minimum quality requirements

### Output Format

Results are output in qBittorrent's expected format:
```
link|name|size|seeds|leech|engine_url|desc_link|pub_date
```

Where:
- `link`: Magnet link or torrent file URL
- `name`: Torrent name
- `size`: File size in bytes
- `seeds`: Number of seeders
- `leech`: Number of leechers
- `engine_url`: Search engine URL (https://bitsearch.to)
- `desc_link`: Link to torrent description page
- `pub_date`: Publication date as Unix timestamp

## Troubleshooting

### Plugin Not Appearing

1. Ensure the filename is exactly `bitsearch.py`
2. Check that the file is in the correct engines directory
3. Restart qBittorrent completely
4. Check qBittorrent logs for any error messages

### No Search Results

1. Verify your internet connection
2. Check if bitsearch.to is accessible from your location
3. Try different search terms
4. Some regions may block access to torrent sites

### Installation Issues

1. Make sure you have Python installed (qBittorrent requirement)
2. Ensure the plugin file has proper permissions
3. Try installing through the GUI method instead of manual copying

## Legal Notice

This plugin is for educational purposes only. Users are responsible for complying with their local laws regarding torrenting and copyright. The plugin author does not endorse or encourage piracy or copyright infringement.

## License

This plugin is released into the public domain. You are free to use, modify, and distribute it as needed.

## Contributing

Feel free to submit improvements, bug fixes, or feature requests. The plugin is designed to be easily maintainable and extensible.

## Testing and Validation

The plugin has been thoroughly tested and validated:

### ✅ Comprehensive Test Results
- **Plugin Structure**: Complies with qBittorrent specification
- **HTML Parsing**: Successfully parses real bitsearch.to data
- **Output Format**: Correct pipe-separated format for qBittorrent
- **Category Support**: All 8 required categories supported
- **Error Handling**: Proper error handling with stderr output
- **Data Extraction**: Accurately extracts names, magnet links, sizes, seeds, leechers

### 🧪 Test Scripts Included
- `test_bitsearch.py` - Basic functionality test
- `test_bitsearch_real.py` - Real HTML parsing test
- `final_test.py` - Comprehensive usability validation

### 📊 How to Determine if Plugin is Working
1. **Structure Compliance**: Class name matches filename, required attributes present
2. **Data Extraction**: Successfully extracts all torrent metadata
3. **Format Compliance**: Outputs in correct qBittorrent format
4. **Error Handling**: Graceful error handling without breaking qBittorrent
5. **Category Support**: All categories work with proper URL construction
6. **Multi-page Support**: Searches multiple pages for comprehensive results

Run `python final_test.py` to validate the plugin is working correctly.

## Version History

- **v1.00**: Initial release
  - Basic search functionality
  - Multi-category support
  - Robust HTML parsing with regex-based extraction
  - Multi-page search results (first 3 pages)
  - Comprehensive error handling
  - Full test suite included