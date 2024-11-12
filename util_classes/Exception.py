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