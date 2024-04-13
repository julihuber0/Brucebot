"""error_message returns various error messages."""


def error_message(error_type: str) -> str:
    """Return an error message based on value."""
    errors = {
        "date": "ERROR: Date Not Specified or Incorrect Format (Date should be in YYYY-MM-DD Format)",  # noqa: E501
        "no-setlist": "No Set Details Found",
        "song": "ERROR: Song Missing from Input",
        "show": "ERROR: Show Not Found",
        "tour": "ERROR: Tour Not Found",
        "cover": "ERROR: Cover Not Found",
        "input": "ERROR: Invalid Input",
        "album": "ERROR: Album Not Found, or Tracks (which is too long for an embed)",
        "relation": "ERROR: Relation Not Found",
        "event": "ERROR: No Event Found for Specified Date",
    }

    return errors.get(error_type)
