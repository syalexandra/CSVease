class LexerDFA:
    def __init__(self,input_string):
        self.tokens = []
        self.position = 0
        self.current_char = input_string[self.position] if input_string else None


    def advance(self):
        self.position += 1
        if self.positions >= len(self.input_string):
            self.current_char = None
        else:
            self.current_char = self.input_string[self.position]

    def isWhiteSpace(ch):
        return ch ==' ' or ch == '\t' or ch =='\n'

    def isKeyWord(ch):


    def isIdentifier(ch):


    def isAlphabet(ch):

    def run(self):
        if self.current_char == ',':
            self.tokens.append(('COMMA',','))
            self.advance()
        elif self.current_char == '.':
            self.tokens.append(('DOT','.'))
            self.advance()
        elif self.current_char == '+':
            self.tokens.append(('PLUS','+'))
            self.advance()
        elif self.current_char == '(':
            self.tokens.append(('LPAR','('))
            self.advance()
        elif self.isWhiteSpace(self.current_char):
            self.tokens.append(('WHITESPACE',self.current_char))
            self.advance()
        
        


