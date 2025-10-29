#!/bin/bash
# run.sh - Shortcut to run scripts with virtual environment activated

if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

source .venv/bin/activate

# Check which script to run
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  check [options]          - One-time playlist checker"
    echo "  watch [options]          - Background watcher"
    echo "  update                   - Auto-discover Spotify playlists"
    echo "  update-csv [options]     - Quick CSV updater (checks downloaded songs)"
    echo ""
    echo "Examples:"
    echo "  ./run.sh check"
    echo "  ./run.sh check --download-folder /path/to/folder"
    echo "  ./run.sh check --manual-verify"
    echo "  ./run.sh check --manual-verify --dont-filter-results"
    echo "  ./run.sh check --manual-link"
    echo "  ./run.sh watch --interval 5"
    echo "  ./run.sh update"
    echo "  ./run.sh update-csv --download-folder /path/to/folder"
    exit 0
fi

SCRIPT=$1
shift  # Remove first argument, pass remaining to script

case $SCRIPT in
    check)
        python src/check.py "$@"
        ;;
    watch)
        python src/watch.py "$@"
        ;;
    update)
        python src/update_playlists_txt.py "$@"
        ;;
    update-csv)
        python src/update_csv.py "$@"
        ;;
    *)
        echo "Unknown command: $SCRIPT"
        echo "Run './run.sh' with no arguments for help."
        exit 1
        ;;
esac
