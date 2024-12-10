class ParserError(Exception):
    pass

class LexerErrors:
    def __init__(self, file):
        self.errors = []
        self.error_count = 0
        self.file = file
        
    # ANSI color codes
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
          
    def UnexpectedCharacter(self, line, lineNo, error):
        self.error_count += 1
        line_info = f"CSVeaseLexer: Line {lineNo}"
        error_info = f"Unexpected character: '{error}'."
        if "\n" in line:
            self.errors.append(f"{line_info} -- {error_info}")
        else:
            self.errors.append(f"{line_info}\n{error_info}")

    def InvalidString(self, line, lineNo, error):
        self.error_count += 1
        line_info = f"CSVeaseLexer: Line {lineNo}:"
        error_info = f"Unterminated string literal: {error}"
        if "\n" in line:
            self.errors.append(f"{line_info}{error_info}")
        else:
            self.errors.append(f"{line_info}\n{error_info}")
    
    def InvalidSequence(self, line, lineNo, error):
        self.error_count += 1 
        line_info = f"CSVeaseLexer: Line {lineNo}:"
        error_info = f"Invalid sequence: `{error}`"
        if "\n" in line:
            self.errors.append(f"{line_info} -- {error_info}")
        else:
            self.errors.append(f"{line_info}\n{error_info}")

    def printErrors(self):
        for error in self.errors:
            print(error)
