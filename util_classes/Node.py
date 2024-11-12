class Node:
    def __init__(self, type: str, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
    
    def __str__(self):
        if self.value and self.value != self.type:
            return f"{self.type}({self.value})"
        elif self.type in ['LPAREN', 'RPAREN', 'EQ', 'COMMA','PLUS']:
            return self.type_to_symbol()
        return self.type
        
    def type_to_symbol(self):
        symbols = {
            'LPAREN': '(',
            'RPAREN': ')',
            'EQ': '=',
            'COMMA': ',',
            'PLUS': '+'
        }
        return symbols.get(self.type, self.type)