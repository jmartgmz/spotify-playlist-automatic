# Project Structure

## Scripts (in `src/`)

- **check.py** - One-time checker: Downloads all missing songs from playlists in `playlists.txt`
- **watch.py** - Background watcher: Periodically checks for and downloads new songs
- **update_playlists_txt.py** - Auto-discovers your Spotify playlists and populates `playlists.txt`
- **update_csv.py** - Updates CSV status files based on current downloads

## Configuration

- **.env** - Your Spotify API credentials (copy from `.env.example`, not committed to git)
- **playlists.txt** - List of Spotify playlist URLs/IDs (one per line, use `#` for comments)
- **requirements.txt** - Python package dependencies

## Folders

- **downloaded_songs/** - Downloaded music, organized by playlist subfolder
- **playlist_songs/** - CSV status reports (Artist, Song Title, Status)
- **src/** - All Python scripts

## Support Modules (in `src/`)

- **spotify_api.py** - Spotify API wrapper
- **file_manager.py** - File operations and song matching
- **downloader.py** - spotdl wrapper for YouTube downloads
- **csv_manager.py** - CSV reading/writing
- **utils.py** - Utilities and user input
- **logger.py** - Logging with color-coded output
- **error_handler.py** - Error handling and validation
- **config.py** - Centralized configuration

