class BadIdentifier(Exception):
    def __init__(self, message="Invalid identifier format."):
        super().__init__(message)

class InvalidSequence(Exception):
    def __init__(self, error):
        self.error=error
        super().__init__(error)

class UnexpectedCharacter(Exception):
    def __init__(self, error):
        self.error=error
        super().__init__(error)

class InvalidString(Exception):
    def __init__(self, error):
        self.error=error
        super().__init__(error)