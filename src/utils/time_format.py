"""Time formatting utilities"""

def format_timestamp(seconds: float, include_hours: bool = True) -> str:
    """
    Format seconds as timestamp

    Args:
        seconds: Time in seconds
        include_hours: Include hours in format

    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    if include_hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    else:
        return f"{minutes:02d}:{secs:02d}.{millis:03d}"


def parse_timestamp(timestamp: str) -> float:
    """
    Parse timestamp string to seconds

    Args:
        timestamp: Timestamp string (HH:MM:SS.mmm or MM:SS.mmm)

    Returns:
        Time in seconds
    """
    parts = timestamp.split(':')

    if len(parts) == 3:  # HH:MM:SS.mmm
        hours, minutes, seconds = parts
        total = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    elif len(parts) == 2:  # MM:SS.mmm
        minutes, seconds = parts
        total = int(minutes) * 60 + float(seconds)
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")

    return total
