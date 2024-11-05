class Node:
    def __init__(self, token, children):
        self.children = children
        self.token = token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
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
    
    def expression(self):
        if self.match([('KEYWORD','LOAD')]):
            return [Node(('KEYWORD','LOAD'), self.loadStatement())]
        elif self.match([('KEYWORD','SHOW')]):
            return [Node(('KEYWORD','SHOW'), self.loadStatement())]
        
    def loadStatement(self):
        ret_nodes = []
        if self.match([('KEYWORD','DATA'),('STRING', None)]):
            operator = self.previous()
            ret_nodes.append(operator)
            if self.match([('KEYWORD','INTO')]):
                operator = self.previous()
                ret_nodes.append(operator)
                if self.match([('IDENTIFIER', None)]):
                    operator = self.previous()
                    ret_nodes.append(operator)
                    return ret_nodes
                else:
                    raise Exception
            else:
                return ret_nodes
            
    def showStatement(self):
        ret_nodes = []
        if self.match([('KEYWORD','ROWS'),('KEYWORD', 'COLUMNS')]):
            operator = self.previous()
            ret_nodes.append(operator)
            if self.match([('KEYWORD','IN')]):
                operator = self.previous()
                ret_nodes.append(operator)
                if self.match([('IDENTIFIER', None)]):
                    operator = self.previous()
                    ret_nodes.append(operator)
                    return ret_nodes
                else:
                    raise Exception
            else:
                raise Exception
        else:
            raise Exception


            



if __name__=='__main__':
    ast = Parser([('KEYWORD','LOAD'),('KEYWORD','DATA'),('KEYWORD','INTO'),('IDENTIFIER','sales_data')]).parse()
    print(ast)


