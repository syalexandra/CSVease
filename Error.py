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
        line_info = f"{self.YELLOW}Line {lineNo}:{self.RESET}"
        error_info = f"{self.RED}ERROR{self.RESET} Unexpected character: '{error}'."
        if "\n" in line:
            self.errors.append(f"{line_info} {line}{error_info}")
        else:
            self.errors.append(f"{line_info} {line}\n{error_info}")

    def InvalidString(self, line, lineNo, error):
        self.error_count += 1
        line_info = f"{self.YELLOW}Line {lineNo}:{self.RESET}"
        error_info = f"{self.RED}ERROR{self.RESET} Unterminated string literal: {error}"
        if "\n" in line:
            self.errors.append(f"{line_info} {line}{error_info}")
        else:
            self.errors.append(f"{line_info} {line}\n{error_info}")
    
    def InvalidSequence(self, line, lineNo, error):
        self.error_count += 1 
        line_info = f"{self.YELLOW}Line {lineNo}:{self.RESET}"
        error_info = f"{self.RED}ERROR{self.RESET} Invalid sequence: `{error}`"
        if "\n" in line:
            self.errors.append(f"{line_info} {line}{error_info}")
        else:
            self.errors.append(f"{line_info} {line}\n{error_info}")

    def printErrors(self):
        if self.error_count > 1:
            print(f"\n{self.RED}There were {self.error_count} errors in {self.file}:{self.RESET}\n")
        else:
            print(f"\n{self.RED}There was {self.error_count} error in {self.file}:{self.RESET}\n")

        for error in self.errors:
            print(error)
