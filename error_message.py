"""
error_message
returns various error messages
"""

def error_message(error_type):
	"""Returns an error message based on value"""
	match(error_type):
		case "date":
			return "ERROR: Date Not Specified or Incorrect Format (Date should be in YYYY-MM-DD Format)"
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
			return "ERROR: Album Not Found"
