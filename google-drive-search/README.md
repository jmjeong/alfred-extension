# Google Drive Search

Alfred workflow to search and open Google Docs, Sheets, Slides, and Drawings from your locally synced Google Drive.

No API key required — reads directly from the Google Drive for Desktop sync directory.

## Usage

- `gd` — list all documents (sorted by last modified)
- `gd <query>` — search by keyword (multiple words are AND-matched)
- Hold `Cmd` to preview the full URL

## How it works

1. Scans `~/Library/CloudStorage/GoogleDrive-*/My Drive/` for `.gdoc`, `.gsheet`, `.gslides`, `.gdraw` files
2. Reads the `com.google.drivefs.item-id` extended attribute to get the document ID
3. Constructs the Google Docs URL and opens it in your default browser
4. Results are cached for 5 minutes (configurable)

## Requirements

- macOS
- [Google Drive for Desktop](https://www.google.com/drive/download/) with file sync enabled
- Python 3
- Alfred with Powerpack

## Configuration

Edit `config.json` in the workflow directory:

```json
{
  "cache_ttl": 300,
  "keyword": "gd"
}
```

- `cache_ttl` — cache duration in seconds (default: 300)
- `keyword` — Alfred trigger keyword (default: "gd")

## Multiple accounts

If you have multiple Google Drive accounts synced, the workflow automatically detects all of them and shows the account name in the subtitle.
