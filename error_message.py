"""
error_message
returns various error messages
"""

def error_message(error_type):
	"""Returns an error message based on value"""
	match(error_type):
		case "date":
			return "ERROR: Date Not Specified or Incorrect Format (Date should be in YYYY-MM-DD Format)"
		case "no-setlist":
			return "No Set Details Found"
		case "song":
			return "ERROR: Song Missing from Input"
		case "show":
			return "ERROR: Show Not Found"
		case "tour":
			return "ERROR: Tour Not Found"
		case "cover":
			return "ERROR: Cover Not Found"
		case "input":
			return "ERROR: Invalid Input"
		case "album":
			return "ERROR: Album Not Found, or Tracks (which is too long for an embed)"
		case "relation":
			return "ERROR: Relation Not Found"
