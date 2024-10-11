class BadIdentifier(Exception):
    def __init__(self, message="Invalid identifier format."):
        super().__init__(message)

class InvalidSequence(Exception):
    def __init__(self, line):
        super().__init__(f"Invalid sequence. {line}")

class UnexpectedCharacter(Exception):
    def __init__(self, message="Unexpected character"):
        super().__init__(message)

class InvalidString(Exception):
    def __init__(self, message="Invalid string format."):
        super().__init__(message)

class LexerErrors:
    def __init__(self):
        self.errors = []
        self.error_count = 0
        
    def BadIdentifier(self, line, lineNo):
        self.error_count += 1
        self.errors.append(f"Line {lineNo}: {line}ERROR: Invalid identifier format")
          
    def UnexpectedCharacter(self, line, lineNo):
        self.error_count += 1
        self.errors.append(f"Line {lineNo}: `{line}ERROR: Unexpected character.")

    def InvalidString(self, line, lineNo):
        self.error_count += 1 
        self.errors.append(f"Line {lineNo}: `{line}ERROR: Invalid string format.")
    
    def InvalidSequence(self, line, lineNo):
        self.error_count += 1 
        self.errors.append(f"Line {lineNo}: `{line}ERROR: Invalid sequence.")
        
    def printErrors(self):
        print(f"There were {self.error_count} errors:")
        for error in self.errors:
            print(error)