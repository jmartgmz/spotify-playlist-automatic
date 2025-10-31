
import os
import subprocess
import sys
import importlib.util

def is_frozen():
    """Check if running as a PyInstaller executable."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# Add spotify_sync directory to path for imports  
spotify_sync_dir = os.path.join(os.path.dirname(__file__), 'spotify_sync')
if os.path.exists(spotify_sync_dir):
    sys.path.insert(0, os.path.dirname(__file__))

# Keep src directory for backward compatibility during transition
src_dir = os.path.join(os.path.dirname(__file__), 'src')
if os.path.exists(src_dir):
    sys.path.insert(0, src_dir)

def show_help():
    """Display detailed help information."""
    print("\n" + "="*70)
    print("SPOTIFY PLAYLIST SYNC - COMMAND HELP")
    print("="*70)
    print("\n📱 COMMANDS:")
    print("  sync (s)     - One-time sync: Download missing songs from playlists")
    print("  watch (w)    - Background watcher: Monitor for new songs continuously")
    print("  discover (d) - Auto-discover Spotify playlists and update playlists.txt")
    print("  refresh (r)  - Quick refresh: Update CSV files with current downloads")
    print("  setup        - Run the setup wizard again (re-configure)")
    print("  help         - Show this help message")
    print("  exit         - Exit the program")
    print("\n🔧 SYNC OPTIONS:")
    print("  --download-folder PATH   - Custom download location")
    print("  --manual-verify          - Ask before downloading each song")
    print("  --manual-link            - Manually provide YouTube links")
    print("  --cleanup-removed        - Prompt to clean up songs removed from playlists")
    print("  --auto-delete-removed    - Auto-delete files for removed songs")
    print("  --keep-removed           - Keep files for removed songs")
    print("\n📝 EXAMPLES:")
    print("  sync                                    - Sync all playlists")
    print("  sync --manual-verify                   - Sync with manual confirmation")
    print("  sync --cleanup-removed                 - Sync and handle removed songs")
    print("  watch --interval 10                    - Watch every 10 minutes")
    print("  discover                               - Auto-discover your playlists")
    print("\n💡 TIPS:")
    print("  • Use short aliases (s, w, d, r) for faster typing")
    print("  • The watcher runs continuously - press Ctrl+C to stop")
    print("  • Use 'discover' first to populate playlists.txt automatically")
    print("  • CSV files track download status for each playlist")
    print("="*70 + "\n")

def suggest_command(user_input):
    """Suggest similar commands when user types something invalid."""
    commands = {
        'sync': ['check', 'download', 'get', 'dl'],
        'watch': ['monitor', 'background', 'auto'],
        'discover': ['update', 'find', 'scan', 'search'],
        'refresh': ['update-csv', 'csv', 'status'],
        'help': ['?', 'h', 'commands'],
        'exit': ['quit', 'q', 'close']
    }
    
    user_input = user_input.lower().strip()
    
    # Direct matches
    for cmd, aliases in commands.items():
        if user_input in aliases:
            return f"Did you mean '{cmd}'? (Type '{cmd}' or 'help' for more info)"
    
    # Partial matches
    for cmd in commands.keys():
        if user_input in cmd or cmd.startswith(user_input):
            return f"Did you mean '{cmd}'? (Type '{cmd}' or 'help' for more info)"
    
    return "Type 'help' to see available commands."

def first_time_setup():
    """Complete first-time setup wizard for the application."""
    print("\n" + "="*70)
    print("🎵 SPOTIFY PLAYLIST SYNC - FIRST TIME SETUP")
    print("="*70)
    print("\nWelcome! Let's set up your Spotify Playlist Sync application.")
    print("This will only take a few minutes.\n")
    
    # Step 1: Spotify API Setup
    print("📋 STEP 1: Spotify API Credentials")
    print("-" * 40)
    print("You'll need to get API credentials from Spotify:")
    print("1. Go to: https://developer.spotify.com/dashboard")
    print("2. Click 'Create an App'")
    print("3. Fill in any name and description")
    print("4. Add this as a Redirect URI: http://127.0.0.1:8888/callback")
    print("5. Copy your Client ID and Client Secret")
    print("")
    
    while True:
        client_id = input("Enter your SPOTIFY_CLIENT_ID: ").strip()
        if client_id:
            break
        print("❌ Client ID cannot be empty. Please try again.")
    
    while True:
        client_secret = input("Enter your SPOTIFY_CLIENT_SECRET: ").strip()
        if client_secret:
            break
        print("❌ Client Secret cannot be empty. Please try again.")
    
    redirect_uri = input("Enter REDIRECT_URI (press Enter for default): ").strip()
    if not redirect_uri:
        redirect_uri = "http://127.0.0.1:8888/callback"
    
    # Create .env file
    with open(".env", "w") as f:
        f.write(f"SPOTIFY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIFY_CLIENT_SECRET={client_secret}\n")
        f.write(f"SPOTIFY_REDIRECT_URI={redirect_uri}\n")
        f.write(f"\n# Optional settings (uncomment to use):\n")
        f.write(f"# DOWNLOADS_FOLDER=downloaded_songs\n")
        f.write(f"# UI_ENABLE_DEBUG_MODE=false\n")
        f.write(f"# UI_ENABLE_TIMESTAMPS=true\n")
    
    print("✅ Credentials saved to .env file")
    
    # Step 2: Download folder setup
    print("\n📁 STEP 2: Download Location")
    print("-" * 40)
    default_folder = "downloaded_songs"
    download_folder = input(f"Download folder (press Enter for '{default_folder}'): ").strip()
    if not download_folder:
        download_folder = default_folder
    
    # Create download folder
    if not os.path.exists(download_folder):
        os.makedirs(download_folder, exist_ok=True)
        print(f"✅ Created download folder: {download_folder}")
    else:
        print(f"✅ Using existing folder: {download_folder}")
    
    # Step 3: Playlists setup
    print("\n🎵 STEP 3: Spotify Playlists")
    print("-" * 40)
    print("You can add playlists in several ways:")
    print("1. Manual entry (recommended for first time)")
    print("2. Auto-discovery (requires authorization)")
    print("3. Skip for now (add to playlists.txt later)")
    
    choice = input("Choose option (1/2/3): ").strip()
    
    playlists = []
    if choice == "1":
        print("\nEnter your Spotify playlist URLs or IDs (one per line).")
        print("Examples:")
        print("  https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        print("  37i9dQZF1DX0XUsuxWHRQd")
        print("Press Enter twice when done.")
        print("")
        
        while True:
            playlist = input("Playlist URL/ID: ").strip()
            if not playlist:
                break
            playlists.append(playlist)
            print(f"✅ Added: {playlist}")
        
        if playlists:
            with open("playlists.txt", "w") as f:
                for playlist in playlists:
                    f.write(f"{playlist}\n")
                f.write(f"\n# Add more playlist URLs or IDs here\n")
                f.write(f"# Examples:\n")
                f.write(f"# https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M\n")
                f.write(f"# 37i9dQZF1DX0XUsuxWHRQd\n")
            print(f"✅ Saved {len(playlists)} playlists to playlists.txt")
        else:
            create_default_playlists_file()
    
    elif choice == "2":
        print("\n🔍 Auto-discovery will be available after first authorization.")
        print("We'll create a basic playlists.txt file for now.")
        create_default_playlists_file()
        print("💡 Use the 'discover' command later to auto-populate playlists.")
    
    else:
        create_default_playlists_file()
    
    # Step 4: Final setup
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 70)
    print("Your Spotify Playlist Sync is ready to use!")
    print("")
    print("📁 Files created:")
    print(f"  • .env - Your API credentials")
    print(f"  • playlists.txt - Your playlist list") 
    print(f"  • {download_folder}/ - Download folder")
    print("")
    print("🚀 Quick start commands:")
    print("  • sync - Download missing songs from your playlists")
    print("  • watch - Monitor playlists for new songs continuously")
    print("  • discover - Auto-discover your Spotify playlists")
    print("  • help - Show all available commands")
    print("")
    print("Let's start downloading your music! 🎵")
    print("")

def create_default_playlists_file():
    """Create a default playlists.txt file with examples."""
    with open("playlists.txt", "w") as f:
        f.write("# Add your Spotify playlist URLs or IDs here\n")
        f.write("# Examples:\n")
        f.write("# https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M\n")
        f.write("# 37i9dQZF1DX0XUsuxWHRQd\n")
        f.write("# spotify:playlist:37i9dQZF1DX4UtSsGT1Sbe\n")
        f.write("\n")
        f.write("# Uncomment a line below to test:\n")
        f.write("# https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M  # Today's Top Hits\n")
    print("✅ Created playlists.txt template")

def prompt_env():
    """Legacy function - redirects to full setup."""
    first_time_setup()

def check_and_create_folders():
    """Ensure all necessary folders exist."""
    folders_to_create = [
        "downloaded_songs",
        "playlist_songs" 
    ]
    
    for folder in folders_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

def main():
    # Ensure necessary folders exist
    check_and_create_folders()
    
    # Check for first-time setup
    needs_setup = False
    if not os.path.exists(".env"):
        needs_setup = True
    elif not os.path.exists("playlists.txt"):
        needs_setup = True
    
    if needs_setup:
        first_time_setup()
    else:
        print("🎵 Spotify Playlist Sync")
        print("All configuration files found. Ready to go!")
        print("")

    # Handle frozen executable playlist input for backwards compatibility
    playlist = None
    if is_frozen() and not os.path.exists("playlists.txt"):
        playlist = input("Enter Spotify playlist URL or ID (leave blank to use playlists.txt): ").strip()
        if playlist:
            # Write playlist to playlists.txt in the current directory
            with open("playlists.txt", "w", encoding="utf-8") as f:
                f.write(playlist + "\n")
                f.write("# Add more playlists above this line\n")
            print("✓ playlists.txt created")

    print("\n" + "="*60)
    print("🎵 SPOTIFY PLAYLIST SYNC - READY TO USE")
    print("="*60)
    print("Type a command (e.g., sync --download-folder /path/to/music)")
    print("")
    print("📋 Available commands:")
    print("  sync, watch, discover, refresh, help, exit")
    print("📝 Aliases: s, w, d, r")
    print("❓ Type 'help' for detailed descriptions")
    print("")

    while True:
        try:
            cmd = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break
        if cmd.lower() in ("exit", "quit", "q"):
            print("👋 Goodbye!")
            break
        if cmd.lower() in ("help", "h", "?"):
            show_help()
            continue
        if cmd.lower() in ("setup", "config", "configure"):
            print("\n🔧 Running setup wizard...")
            first_time_setup()
            continue
        if not cmd:
            continue
        if is_frozen():
            # Directly import and call the script functions when running as an exe
            parts = cmd.split()
            if not parts:
                continue
            command = parts[0].lower()
            args = parts[1:]
            
            try:
                script_map = {
                    "sync": "check.py",
                    "check": "check.py",  # Backward compatibility
                    "s": "check.py",      # Short alias
                    "watch": "watch.py",
                    "w": "watch.py",      # Short alias
                    "discover": "update_playlists_txt.py",
                    "update": "update_playlists_txt.py",  # Backward compatibility
                    "d": "update_playlists_txt.py",       # Short alias
                    "refresh": "update_csv.py",
                    "update-csv": "update_csv.py",        # Backward compatibility
                    "r": "update_csv.py"                  # Short alias
                }
                
                script_name = script_map.get(command)
                if not script_name:
                    print(f"❌ Unknown command: '{command}'")
                    print(f"💡 {suggest_command(command)}")
                    continue
                
                # When frozen, try to import modules directly instead of file paths
                module_map = {
                    "check.py": "spotify_sync.commands.check",
                    "watch.py": "spotify_sync.commands.watch", 
                    "update_playlists_txt.py": "spotify_sync.commands.update_playlists_txt",
                    "update_csv.py": "spotify_sync.commands.update_csv"
                }
                
                module_name = module_map.get(script_name)
                if module_name:
                    try:
                        # Try to import and run the module directly
                        module = __import__(module_name, fromlist=[''])
                        
                        # Set sys.argv for argparse
                        sys.argv = [module_name] + args
                        if playlist:
                            sys.argv.append(playlist)
                        
                        print(f"[DEBUG] Running module {module_name} with args: {sys.argv}")
                        # Execute main function
                        if hasattr(module, 'main'):
                            module.main()
                        else:
                            print(f"Error: Module {module_name} has no main() function")
                        continue
                    except ImportError as e:
                        print(f"[DEBUG] Failed to import module {module_name}: {e}")
                        # Fall back to file-based loading
                        pass
                
                # Fallback: Find the script file - try new structure first, then fallback to old
                script_path = os.path.join(spotify_sync_dir, "commands", script_name)
                if not os.path.exists(script_path):
                    # Fallback to old src structure during transition
                    script_path = os.path.join(src_dir, script_name)
                
                print(f"[DEBUG] Looking for script at: {script_path}")
                
                if not os.path.exists(script_path):
                    print(f"Error: Script {script_name} not found at {script_path}")
                    print(f"[DEBUG] spotify_sync_dir is: {spotify_sync_dir}")
                    print(f"[DEBUG] src_dir is: {src_dir}")
                    if os.path.exists(spotify_sync_dir):
                        print(f"[DEBUG] Contents of spotify_sync_dir: {os.listdir(spotify_sync_dir)}")
                    if os.path.exists(src_dir):
                        print(f"[DEBUG] Contents of src_dir: {os.listdir(src_dir)}")
                    continue
                
                # Load the module dynamically
                module_name = script_name.replace(".py", "")
                print(f"[DEBUG] Loading module: {module_name} from {script_path}")
                
                spec = importlib.util.spec_from_file_location(module_name, script_path)
                if spec is None or spec.loader is None:
                    print(f"Error: Could not load {script_name}")
                    continue
                    
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                
                # Set sys.argv for argparse
                sys.argv = [module_name] + args
                if playlist:
                    sys.argv.append(playlist)
                
                print(f"[DEBUG] Executing module with sys.argv: {sys.argv}")
                # Execute the module
                spec.loader.exec_module(module)
                print(f"[DEBUG] Module execution completed")
                
            except Exception as e:
                import traceback
                print(f"Error running command: {e}")
                print(f"[DEBUG] Full traceback:")
                traceback.print_exc()
        else:
            # Use appropriate run script for normal (non-frozen) usage
            import platform
            if platform.system() == "Windows":
                full_cmd = ["cmd", "/c", "scripts\\run.bat"] + cmd.split()
            else:
                full_cmd = ["./scripts/run.sh"] + cmd.split()
            subprocess.call(full_cmd)

if __name__ == "__main__":
    main()
