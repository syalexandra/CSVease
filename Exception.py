class BadIdentifier(Exception):
    def __init__(self, message="Invalid identifier format."):
        super().__init__(message)

class InvalidSequence(Exception):
    def __init__(self, line):
        super().__init__(f"Invalid sequence. {line}")

class UnexpectedCharacter(Exception):
    def __init__(self, character):
        super().__init__(f"Unexpected character: {character}")

class InvalidString(Exception):
    def __init__(self, message="Invalid string format."):
        super().__init__(message)