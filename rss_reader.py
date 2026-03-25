from argparse import ArgumentParser
from html import unescape
import json
from typing import Dict, List, Optional, Sequence
import xml.etree.ElementTree as ET

import requests


class UnhandledException(Exception):
    pass


CHANNEL_TITLES = {
    "title": "Feed",
    "link": "Link",
    "lastBuildDate": "Last Build Date",
    "pubDate": "Publish Date",
    "language": "Language",
    "category": "Categories",
    "managingEditor": "Editor",
    "description": "Description",
}

ITEM_TITLES = {
    "title": "Title",
    "author": "Author",
    "pubDate": "Published",
    "link": "Link",
    "category": "Categories",
    "description": "Description",
}


def _get_categories(
    rss_object: ET.Element,
) -> Optional[str]:
    categories = [
        unescape(category.text).strip()
        for category in rss_object.findall("category")
        if category.text and category.text.strip()
    ]
    return ", ".join(categories) if categories else None


def _get_text(
    rss_object: Optional[ET.Element],
) -> Optional[str]:
    if (rss_object is None) or (rss_object.text is None):
        return None

    text = unescape(rss_object.text).strip()
    return text or None


def _collect_channel_data(channel: ET.Element) -> Dict:
    data: Dict = {}

    for tag in CHANNEL_TITLES:
        if tag == "category":
            categories = _get_categories(channel)
            if categories:
                data[tag] = categories
            continue

        text = _get_text(channel.find(tag))
        if text:
            data[tag] = text

    data["items"] = []
    return data


def _collect_item_data(item: ET.Element) -> Dict:
    item_data: Dict = {}

    for tag in ITEM_TITLES:
        if tag == "category":
            categories = _get_categories(item)
            if categories:
                item_data[tag] = categories
            continue

        text = _get_text(item.find(tag))
        if text:
            item_data[tag] = text

    return item_data


def _format_plain_output(data: Dict) -> str:
    lines: List[str] = []

    for tag in CHANNEL_TITLES:
        if tag in data:
            lines.append(f"{CHANNEL_TITLES[tag]}: {data[tag]}")

    items = data.get("items", [])
    if items:
        lines.append("")

    for index, item in enumerate(items):
        for tag in ITEM_TITLES:
            if tag not in item:
                continue

            if tag == "description":
                lines.append("")
                lines.append(item[tag])
            else:
                lines.append(f"{ITEM_TITLES[tag]}: {item[tag]}")

        if index != (len(items) - 1):
            lines.append("")

    return "\n".join(lines)


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    is_json: bool = False,
) -> str:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. If None, returns all news.
        is_json: If True, format output as JSON.

    Returns:
        String.
        Which then can be printed to stdout or written to file.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        >>> print(rss_parser(xml))
        Feed: Some RSS Channel
        Link: https://some.rss.com
        Description: Some RSS Channel
    """
    root = ET.fromstring(xml)
    channel = root.find("channel")

    if channel is None:
        raise ValueError("Invalid RSS feed: <channel> element is missing")

    result = _collect_channel_data(channel)

    for item in channel.findall("item")[:limit]:
        item_data = _collect_item_data(item)
        if item_data:
            result["items"].append(item_data)

    if is_json:
        return json.dumps(result, indent=2, ensure_ascii=False)

    return _format_plain_output(result)


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str)
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )
    try:
        args = parser.parse_args(argv)
        response = requests.get(args.source, timeout=30)
        response.raise_for_status()
        xml = response.text
        print(rss_parser(xml, args.limit, args.json))
        return 0
    except Exception as e:
        raise UnhandledException(e) from e


if __name__ == "__main__":
    main()
