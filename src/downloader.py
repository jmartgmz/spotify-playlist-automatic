"""
Downloader module for spotdl operations.
Handles downloading songs from Spotify/YouTube URLs.
"""

import subprocess
import shutil
import sys
import os
from typing import Optional


class SpotdlDownloader:
    """Manages spotdl download operations."""

    @staticmethod
    def find_spotdl() -> str:
        """
        Find spotdl executable in PATH or virtualenv.
        
        Returns:
            Path to spotdl executable
            
        Raises:
            RuntimeError: If spotdl is not found
        """
        spotdl_path = shutil.which('spotdl')
        if spotdl_path:
            return spotdl_path
        
        venv_spotdl = os.path.join(os.path.dirname(sys.executable), 'spotdl')
        if os.path.exists(venv_spotdl):
            return venv_spotdl
        
        raise RuntimeError("spotdl not found. Please install spotdl in your environment.")

    @staticmethod
    def get_youtube_url(track: dict, dont_filter: bool = False) -> Optional[str]:
        """
        Get the YouTube URL for a song using spotdl url command.
        
        Args:
            track: Track dictionary with 'url' key
            dont_filter: Whether to disable result filtering
            
        Returns:
            YouTube URL or None if not found
        """
        try:
            spotdl_path = SpotdlDownloader.find_spotdl()
            cmd = [spotdl_path, 'url', track['url']]
            if dont_filter:
                cmd.append('--dont-filter-results')
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            youtube_url = result.stdout.strip()
            return youtube_url if youtube_url else None
        except Exception as e:
            print(f"Failed to get YouTube URL for {track['name']}: {e}")
            return None

    @staticmethod
    def download_from_youtube(youtube_url: str, download_folder: str) -> bool:
        """
        Download a song from a YouTube URL using spotdl.
        
        Args:
            youtube_url: YouTube URL to download from
            download_folder: Folder to save the download
            
        Returns:
            True if successful, False otherwise
        """
        try:
            spotdl_path = SpotdlDownloader.find_spotdl()
            subprocess.run([
                spotdl_path, youtube_url, '--output', download_folder
            ], check=True)
            return True
        except Exception as e:
            print(f"Failed to download from YouTube link: {e}")
            return False

    @staticmethod
    def download_from_spotify(track: dict, download_folder: str, dont_filter: bool = False) -> bool:
        """
        Download a song from Spotify URL using spotdl.
        
        Args:
            track: Track dictionary with 'url' key
            download_folder: Folder to save the download
            dont_filter: Whether to disable result filtering
            
        Returns:
            True if successful, False otherwise
        """
        try:
            spotdl_path = SpotdlDownloader.find_spotdl()
            cmd = [spotdl_path, track['url'], '--output', download_folder]
            if dont_filter:
                cmd.append('--dont-filter-results')
            
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            print(f"Failed to download {track['name']}: {e}")
            return False
