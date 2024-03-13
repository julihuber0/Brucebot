"""
error_message
returns various error messages
"""


def error_message(error_type):
    """Returns an error message based on value"""
    match (error_type):
        case "date":
            return "Please provide a valid date (Date should be in YYYY-MM-DD Format)"
        case "no-setlist":
            return "No Set Details Found"
        case "song":
            return "This song could not be found"
        case "show":
            return "This show could not be found"
        case "tour":
            return "This tour could not be found"
        case "cover":
            return "This cover could not be found"
        case "input":
            return "Please provide a valid input"
        case "album":
            return "This album could not be found, or Tracks (which is too long for an embed)"
        case "relation":
            return "This relation could not be found"
        case "event":
            return "There is no event for that specific date"
