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
        self.LL1 = {("S", 'LOAD'): [Entry(True, ('LOAD', 'LOAD')), Entry(False, "A")],
                    ("A", 'DATA'): [Entry(True, ('DATA', 'DATA')), Entry(False, "Aa")],
                    ("A", 'STRING'): [Entry(True, ('STRING', None)), Entry(False, "Aa")],
                    ("Aa", '$'): None,
                    ("Aa",'INTO'): [Entry(True, ('INTO', 'INTO')), Entry(False, "Aaa")],
                    ("Aaa",'IDENTIFIER'):[Entry(True, ('IDENTIFIER', None)), Entry(False, "Aaaa")],
                    ("Aaaa", '$'): None,
                    ("S", 'SHOW'): [Entry(True, ('SHOW', 'SHOW')), Entry(False, "B")],
                    ("B", 'ROWS'): [Entry(True, ('ROWS', 'ROWS')), Entry(False, "Ba")],
                    ("B", 'COLUMNS'): [Entry(True, ('COLUMNS', 'COLUMNS')), Entry(False, "Bb")],
                    ("Ba", 'IN'): [Entry(True, ('IN', 'IN')), Entry(False, "Baa")],
                    ("Baa", 'IDENTIFIER'): [Entry(True, ('IDENTIFIER', None)), Entry(False, "Baaa")],
                    ("Baaa", '$'): None,
                    ("Bb", 'IN'): [Entry(True, ('IN', 'IN')), Entry(False, "Bba")],
                    ("Bba", 'IDENTIFIER'): [Entry(True, ('IDENTIFIER', None)), Entry(False, "Bbaa")],
                    ("Bbaa", '$'): None,
                    ("S", "GET"): [Entry(True, ("GET", "GET")), Entry(False, "C")],
                    ("C", "INTEGER"): [Entry(True, ("INTEGER", None)), Entry(False, "Ca")],
                    ("Ca", "ROWS"): [Entry(True, ("ROWS", "ROWS")), Entry(False, "Caa")],
                    ("Caa", "FROM"): [Entry(True, ("FROM", "FROM")), Entry(False, "Caaa")],
                    ("C", "IDENTIFIER"): [Entry(True, ("IDENTIFIER", None)), Entry(False, "Cb")],
                    ("Cb", "PLUS"): [Entry(True, ("PLUS", "PLUS")), Entry(False, "C")],
                    ("Cb", "FROM"): [Entry(True, ("FROM", "FROM")), Entry(False, "Cba")],
                    ("Cba", "IDENTIFIER"): [Entry(True, ("IDENTIFIER", None)), Entry(False, "Cbaa")],
                    ("Cbaa", '$'): None,
                    ('S', 'IDENTIFIER'): [Entry(True, ('IDENTIFIER', None)), Entry(False, 'X')],
                    ('X', 'EQ'): [Entry(True, ('EQ', '=')), Entry(False, 'S')],

                    }
        
    def peek(self):
        return self.tokens[self.current]
    
    def lookahead(self):
        return self.tokens[self.current + 1]
    
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
        if entryList is None:
            return None
        ret_list = []
        for entry in entryList:
            if entry.isTerminal == True:
                nextToken = self.peek()
                ret_list.append(Node(nextToken, None))
            else:
                self.advance()
                nextToken = self.peek()
                nextEntryList = self.LL1[(entry.value, nextToken[0])]
                node = self.buildNode(nextEntryList)
                if node:
                    ret_list.append(node)
        return ret_list

    def buildASTfromLL1(self):
        terminal = 'S'
        currentToken = self.peek()
        entryList = self.LL1[(terminal, currentToken[0])]
        root = self.buildNode(entryList)
        return root


if __name__=='__main__':
    ast = Parser([('LOAD','LOAD'),('DATA','DATA'),('INTO','INTO'),('IDENTIFIER','sales_data'), ('$', '$')]).buildASTfromLL1()
    print(ast)
    ast = Parser([('LOAD','LOAD'),('STRING','data.csv'), ('$', '$')]).buildASTfromLL1()
    print(ast)
    ast = Parser([('IDENTIFIER','table1'),('EQ','='), ('LOAD', 'LOAD'), ("STRING", 'data.csv'), ('$', '$')]).buildASTfromLL1()
    print(ast)
    ast = Parser([('GET','GET'),('IDENTIFIER','COLUMN1'), ('PLUS', '+'), ("IDENTIFIER", 'COLUMN2'), ('PLUS', '+'), ("IDENTIFIER", 'COLUMN3'), ("FROM", 'FROM'), ("IDENTIFIER", 'TABLE1'),('$', '$')]).buildASTfromLL1()
    print(ast)


