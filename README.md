# Spotify Playlist Automatic Downloader

Automatically download songs from Spotify playlists with one-time checks or continuous monitoring.

## Quick Start

**1. Run the setup script (easiest way):**
```bash
./setup.sh
```

This automatically:
- ✅ Creates a Python virtual environment
- ✅ Installs all dependencies
- ✅ Creates `.env` template and `playlists.txt`
- ✅ Shows next steps

**2. Add your Spotify credentials:**
Edit `.env` and add your Spotify API credentials from https://developer.spotify.com/dashboard

**3. Add playlists:**
Run auto-discovery:
```bash
source .venv/bin/activate
python src/update_playlists_txt.py
```
Or manually edit `playlists.txt` with playlist URLs/IDs

## Usage

**Activate environment first:**
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**Run commands:**

```bash
# One-time: Download all missing songs
python src/check.py

# Watch: Check every 10 minutes for new songs
python src/watch.py --interval 10

# Auto-discover: Populate playlists.txt from your Spotify account
python src/update_playlists_txt.py

# Update CSVs: Sync CSV files with current downloads
python src/update_csv.py

# Custom download folder
python src/check.py --download-folder /path/to/folder
```

**Options for check.py:**
- `--download-folder FOLDER` - Save downloads to custom location
- `--manual-verify` - Show YouTube match and ask to confirm before downloading
- `--manual-link` - Manually provide YouTube links for each song
- `--dont-filter-results` - Disable spotdl result filtering

## Preferred Usage: Shortcuts with run.sh

The easiest way to use this project is with the `run.sh` script:

```bash
./run.sh check                  # One-time check
./run.sh watch --interval 5     # Watcher with 5-min interval
./run.sh update                 # Auto-discover playlists
./run.sh update-csv             # Update CSVs
./run.sh check --download-folder /path/to/folder  # Custom folder
```

All options for `check`, `watch`, and other commands are supported via `run.sh`.

## Output

- **Downloaded songs:** `downloaded_songs/` (organized by playlist)
- **Status reports:** `playlist_songs/` (CSV files with download status)

## Documentation

- 📋 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project layout and module descriptions
- 🔑 **[GETTING_SPOTIFY_API.md](GETTING_SPOTIFY_API.md)** - Detailed Spotify API setup guide

## Notes

- WSL users: Use Windows paths like `C:\Users\...\Downloads`
- Watcher runs forever; press `Ctrl+C` to stop
- Songs are organized into subfolders by playlist name
