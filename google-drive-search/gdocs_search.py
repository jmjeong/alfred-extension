#!/usr/bin/env python3
"""Alfred Script Filter: Search Google Drive synced files and open in browser."""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_CONFIG = {
    "cache_ttl": 300,
    "keyword": "gd",
}

EXTENSIONS = {
    ".gdoc": ("document", "doc.png"),
    ".gsheet": ("spreadsheets", "sheet.png"),
    ".gslides": ("presentation", "slide.png"),
    ".gdraw": ("drawings", "draw.png"),
}

XATTR_KEY = "com.google.drivefs.item-id#S"


def load_config():
    """Load configuration from config.json, falling back to defaults."""
    config = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config.update(json.load(f))
    return config


def find_drive_roots():
    """Auto-detect all Google Drive sync directories."""
    roots = []
    cloud_storage = os.path.expanduser("~/Library/CloudStorage")
    if os.path.isdir(cloud_storage):
        for name in sorted(os.listdir(cloud_storage)):
            if name.startswith("GoogleDrive"):
                my_drive = os.path.join(cloud_storage, name, "My Drive")
                if os.path.isdir(my_drive):
                    account = name.replace("GoogleDrive-", "")
                    roots.append((my_drive, account))
    return roots


def get_item_id(filepath):
    """Extract Google Drive item ID from extended attributes."""
    try:
        result = subprocess.run(
            ["xattr", "-p", XATTR_KEY, filepath],
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def build_url(item_id, ext):
    """Build Google Docs/Sheets/Slides URL from item ID."""
    doc_type = EXTENSIONS.get(ext, ("document",))[0]
    return f"https://docs.google.com/{doc_type}/d/{item_id}/edit"


def find_google_files(roots):
    """Find all Google Docs/Sheets/Slides files recursively across all accounts."""
    items = []
    single_account = len(roots) == 1
    for root, account in roots:
        root_path = Path(root)
        for ext in EXTENSIONS:
            for filepath in root_path.rglob(f"*{ext}"):
                name = filepath.stem
                rel_path = str(filepath.relative_to(root_path).parent)
                folder = rel_path if rel_path != "." else "My Drive"
                if single_account:
                    subtitle_prefix = folder
                else:
                    subtitle_prefix = f"{account}  |  {folder}"
                item_id = get_item_id(str(filepath))
                if not item_id:
                    continue
                url = build_url(item_id, ext)
                icon_file = EXTENSIONS[ext][1]
                mtime = filepath.stat().st_mtime
                mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                items.append(
                    {
                        "title": name,
                        "subtitle": f"{mtime_str}  |  {subtitle_prefix}  |  {ext[1:]}",
                        "arg": url,
                        "icon": {"path": icon_file},
                        "match": name.replace("-", " ").replace("_", " "),
                        "mods": {
                            "cmd": {
                                "subtitle": url,
                                "arg": url,
                            }
                        },
                        "_mtime": mtime,
                    }
                )
    # Sort by last modified time (newest first)
    items.sort(key=lambda x: x["_mtime"], reverse=True)
    return items


def filter_items(items, query):
    """Filter items by query (case-insensitive, all words must match)."""
    if not query:
        return items
    words = query.lower().split()
    return [
        item
        for item in items
        if all(w in item["title"].lower() or w in item["subtitle"].lower() for w in words)
    ]


def main():
    config = load_config()
    query = sys.argv[1] if len(sys.argv) > 1 else ""

    # Use cache file for performance
    cache_dir = os.environ.get(
        "alfred_workflow_cache",
        os.path.expanduser("~/Library/Caches/com.runningwithcrayons.Alfred/Workflow Data/google-drive-search"),
    )
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "files.json")

    # Cache expires after configured TTL
    cache_valid = False
    if os.path.exists(cache_file):
        import time
        cache_valid = (time.time() - os.path.getmtime(cache_file)) < config["cache_ttl"]

    drive_roots = find_drive_roots()

    if not drive_roots:
        print(json.dumps({"items": [{"title": "Google Drive not found", "subtitle": "No GoogleDrive directory in ~/Library/CloudStorage", "valid": False}]}))
        return

    if cache_valid:
        with open(cache_file, "r") as f:
            items = json.load(f)
    else:
        items = find_google_files(drive_roots)
        with open(cache_file, "w") as f:
            json.dump(items, f, ensure_ascii=False)

    filtered = filter_items(items, query)

    if not filtered:
        filtered = [
            {
                "title": "No results found",
                "subtitle": f'No documents matching "{query}"',
                "valid": False,
            }
        ]

    print(json.dumps({"items": filtered}, ensure_ascii=False))


if __name__ == "__main__":
    main()
