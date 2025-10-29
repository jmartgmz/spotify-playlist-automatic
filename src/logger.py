"""
Logging utilities for consistent output formatting and progress tracking.
Provides color-coded messages and progress indicators.
"""

import sys
from enum import Enum


class MessageType(Enum):
    """Message types with color codes."""
    INFO = "\033[94m"      # Blue
    SUCCESS = "\033[92m"   # Green
    WARNING = "\033[93m"   # Yellow
    ERROR = "\033[91m"     # Red
    RESET = "\033[0m"      # Reset color


class Logger:
    """Provides consistent logging with color support."""
    
    ENABLE_COLORS = sys.stdout.isatty()  # Only use colors if terminal supports it

    @staticmethod
    def _format_message(message_type: MessageType, message: str, prefix: str = "") -> str:
        """Format a message with color and prefix."""
        if not Logger.ENABLE_COLORS:
            return f"{prefix}{message}"
        
        color = message_type.value
        reset = MessageType.RESET.value
        return f"{color}{prefix}{message}{reset}"

    @staticmethod
    def info(message: str) -> None:
        """Log an info message."""
        print(Logger._format_message(MessageType.INFO, message, "ℹ "))

    @staticmethod
    def success(message: str) -> None:
        """Log a success message."""
        print(Logger._format_message(MessageType.SUCCESS, message, "✓ "))

    @staticmethod
    def warning(message: str) -> None:
        """Log a warning message."""
        print(Logger._format_message(MessageType.WARNING, message, "⚠ "))

    @staticmethod
    def error(message: str) -> None:
        """Log an error message."""
        print(Logger._format_message(MessageType.ERROR, message, "✗ "))

    @staticmethod
    def header(message: str) -> None:
        """Log a section header."""
        print(f"\n{'='*60}")
        print(Logger._format_message(MessageType.INFO, message))
        print(f"{'='*60}\n")

    @staticmethod
    def progress(current: int, total: int, item_name: str = "") -> None:
        """Log progress with a simple counter."""
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 20
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        
        item_str = f" {item_name}" if item_name else ""
        print(Logger._format_message(
            MessageType.INFO,
            f"[{bar}] {current}/{total} ({percentage:.0f}%){item_str}"
        ))

    @staticmethod
    def section(message: str) -> None:
        """Log a section divider."""
        print(f"\n--- {message} ---")

    @staticmethod
    def summary(label: str, value: str, success: bool = True) -> None:
        """Log a summary line."""
        msg_type = MessageType.SUCCESS if success else MessageType.WARNING
        print(Logger._format_message(msg_type, f"{label}: {value}"))
