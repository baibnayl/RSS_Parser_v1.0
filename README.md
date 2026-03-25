# RSS_Parser_v1.0

A small command-line RSS reader written in Python.

This project fetches an RSS 2.0 feed from a given URL, parses the XML, and prints the result either as formatted plain text or as JSON.

## Features

- Fetches RSS XML from the web
- Parses RSS 2.0 feeds
- Supports formatted console output
- Supports JSON output
- Supports limiting the number of news items
- Decodes escaped HTML entities such as `&#39;` and `&amp;`

## Requirements

- Python 3.10+
- `requests`

## Installation

Clone the repository:

```bash
git clone https://github.com/baibnayl/RSS_Parser_v1.0.git
cd RSS_Parser_v1.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python rss_reader.py SOURCE [--json] [--limit LIMIT]
```

Arguments:
- SOURCE - RSS feed URL<br />
- --json - print output in JSON format<br />
- --limit LIMIT - limit the number of news items returned

## Examples

### Plain text output

```bash
python rss_reader.py https://rss.nytimes.com/services/xml/rss/nyt/World.xml
```

### Limit the number of items

```bash
python rss_reader.py https://rss.nytimes.com/services/xml/rss/nyt/World.xml --limit 5
```

### JSON output

```bash
python rss_reader.py https://rss.nytimes.com/services/xml/rss/nyt/World.xml --json
```

### JSON output with limit
```bash
python rss_reader.py https://rss.nytimes.com/services/xml/rss/nyt/World.xml --json --limit 3
```

## Output Formats

Plain text:<br />
The reader formats channel and item data into a human-readable output.
Example:

```bash
Feed: NYT > World News
Link: https://rss.nytimes.com/services/xml/rss/nyt/World.xml
Description: NYT > World News description

Title: Some News Title
Published: Sun, 25 Mar 2026 04:21:44 +0300
Link: https://example.com/news

Some news description.
```

JSON:<br />
When the --json flag is provided, the reader outputs a pretty-printed JSON string with an indentation of 2 spaces.
Example:

```bash
{
  "title": "NYT > World News",
  "link": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
  "description": "NYT > World News description",
  "items": [
    {
      "title": "Some News Title",
      "pubDate": "Sun, 25 Mar 2026 04:21:44 +0300",
      "link": "https://example.com/news",
      "description": "Some news description."
    }
  ]
}
```

## Project Structure

```bash
rss_reader.py
```

Main parts of the implementation:
- XML parsing with xml.etree.ElementTree
- HTTP requests with requests
- HTML entity decoding with html.unescape
- Separate data collection and output formatting logic

## Design Notes

This project is intentionally structured in small helper functions to keep responsibilities separated:
- extracting plain text from XML elements
- collecting categories
- collecting channel data
- collecting item data
- formatting plain text output
- generating JSON output

This makes the code easier to read, test, and extend.

## Error Handling

The program validates:
- HTTP response status
- RSS channel presence
- request timeout behavior

If the feed is invalid or the request fails, an exception is raised.
