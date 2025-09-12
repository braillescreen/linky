# Linky NVDA Add-on

A simple NVDA add-on that opens the last spoken link with a keyboard shortcut.

## Features

- Automatically captures speech from NVDA
- Maintains a history of up to 500 recent spoken items
- Detects URLs in spoken text
- Opens the most recent link with Ctrl+NVDA+L (by default)

## Usage
1. Install the add-on
2. Navigate web pages or listen to text with links
3. Press Ctrl+NVDA+L to open the last spoken link

## Supported URL Formats
- `http://example.com`
- `https://example.com`
- `www.example.com` (automatically adds https://)

## Building from Source
1. Install python and uv
2. Run `uv run python build.py` in the project directory  
3. Install the generated `.nvda-addon` file
