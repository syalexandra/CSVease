class Node:
    def __init__(self, token, children):
        self.token = token
        self.children = children

class Entry:
    # if it is a terminal, value is the token, if it is not a terminal, value is a string
    def __init__(self, isTerminal, value):
        self.isTerminal = isTerminal
        self.value = value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.LL1 = {("S", ('KEYWORD', 'LOAD')): [Entry(True, ('KEYWORD', 'LOAD')), Entry(False, "A")],
                    ("A", ('KEYWORD', 'DATA')): [Entry(True, ('KEYWORD', 'DATA')), Entry(False, "Aa")],
                    ("A", ('STRING', None)): [Entry(True, ('STRING', None)), Entry(False, "Aa")],
                    ("Aa", ('END', '$')): [],
                    ("Aa",('KEYWORD', 'INTO')): [Entry(True, ('KEYWORD', 'INTO')), Entry(True, ('IDENTIFIER', None))],
                    }
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def advance(self):
        self.current += 1
    
    def match(self, tokenList):
        currentToken = self.peek()
        for token in tokenList:
            if currentToken[0] == token[0]:
                if token[1] is None or currentToken[1] == token[1]:
                    self.advance()
                    return True
        return False
    
    def parse(self):
        return self.expression()


    def buildNode(self, entryList):
        ret_list = []
        for entry in entryList:
            if entry.isTerminal == True:
                token = entry.value
                ret_list.append(Node(token, None))
            else:
                self.advance()
                nextToken = self.peek()
                nextEntryList = self.LL1[(entry.value, nextToken)]
                ret_list.append(self.buildNode(nextEntryList))
        return ret_list

    def buildASTfromLL1(self):
        terminal = 'S'
        currentToken = self.peek()
        entryList = self.LL1[(terminal, currentToken)]
        root = self.buildNode(entryList)
        return root


if __name__=='__main__':
    ast = Parser([('KEYWORD','LOAD'),('KEYWORD','DATA'),('KEYWORD','INTO'),('IDENTIFIER','sales_data')]).buildASTfromLL1()
    print(ast)
    ast = Parser([('KEYWORD','LOAD'),('KEYWORD','DATA'), ('END', '$')]).buildASTfromLL1()
    print(ast)

