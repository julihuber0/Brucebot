def errorMessage(type):
  match(type):
    case "date":
      return "ERROR: Date Not Specified or Incorrect Format"
    case "song":
      return "ERROR: Song Missing from Input"
    case "show":
      return "ERROR: Show Not Found"
    case "cover":
      return "ERROR: Cover Not Found"