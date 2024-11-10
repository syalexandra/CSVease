from typing import Any, Dict, List, Optional, Tuple
from Error import ParserError
from enum import Enum, auto

class TokenType(Enum):
    LOAD = auto()
    DATA = auto()
    STRING = auto()
    INTO = auto()
    IDENTIFIER = auto()
    SHOW = auto()
    ROWS = auto()
    COLUMNS = auto()
    IN = auto()
    GET = auto()
    INTEGER = auto()
    FROM = auto()
    PLUS = auto()
    EQ = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class ASTNode:
    type: str
    value: Any
    children: List['ASTNode']
    token: Optional[Token] = None
    
    def __str__(self):
        return self._str_helper()
    
    def _str_helper(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.type}"
        if self.value:
            result += f": {self.value}"
        if self.children:
            result += "\n" + "\n".join(child._str_helper(level + 1) for child in self.children)
        return result

# class Node:
#     def __init__(self, token, children):
#         self.token = token
#         self.children = children

class Entry:
    # if it is a terminal, value is the token, if it is not a terminal, value is a string
    def __init__(self, isTerminal, value):
        self.isTerminal = isTerminal
        self.value = value


class Parser:
    def __init__(self, tokens):
        if not tokens:
            raise ParserError("Empty token stream")
        if tokens[-1][0] != '$':
            raise ParserError("Token stream must end with EOF ($) token")
        self.tokens = [Token(TokenType[type_], value, line, col) for type_, value, line, col in tokens]
        self.current = 0

        self.LL1: Dict[Tuple[str, TokenType], List[Entry]] = {
            ("S", TokenType.LOAD): [
                Entry(True, (TokenType.LOAD, "LOAD")), 
                Entry(False, "A")
            ],
            ("A", TokenType.DATA): [
                Entry(True, (TokenType.DATA, "DATA")), 
                Entry(False, "Aa")
            ],
            ("A", TokenType.STRING): [
                Entry(True, (TokenType.STRING, None)), 
                Entry(False, "Aa")
            ],
            ("Aa", TokenType.INTO): [
                Entry(True, (TokenType.INTO, "INTO")), 
                Entry(False, "Aaa")
            ],
            ("Aaa", TokenType.IDENTIFIER): [
                Entry(True, (TokenType.IDENTIFIER, None)), 
                Entry(False, "Aaaa")
            ],
            ("Aaaa", TokenType.EOF): None,
            
            ("S", TokenType.SHOW): [
                Entry(True, (TokenType.SHOW, "SHOW")), 
                Entry(False, "B")
            ],
            ("B", TokenType.ROWS): [
                Entry(True, (TokenType.ROWS, "ROWS")), 
                Entry(False, "Ba")
            ],
            ("B", TokenType.COLUMNS): [
                Entry(True, (TokenType.COLUMNS, "COLUMNS")), 
                Entry(False, "Bb")
            ],
            ("Ba", TokenType.IN): [
                Entry(True, (TokenType.IN, "IN")), 
                Entry(False, "Baa")
            ],
            ("Baa", TokenType.IDENTIFIER): [
                Entry(True, (TokenType.IDENTIFIER, None)), 
                Entry(False, "Baaa")
            ],
            ("Baaa", TokenType.EOF): None,
            
            ("S", TokenType.GET): [
                Entry(True, (TokenType.GET, "GET")), 
                Entry(False, "C")
            ],
            ("C", TokenType.INTEGER): [
                Entry(True, (TokenType.INTEGER, None)), 
                Entry(False, "Ca")
            ],
            ("C", TokenType.IDENTIFIER): [
                Entry(True, (TokenType.IDENTIFIER, None)), 
                Entry(False, "Cb")
            ],
            ("Ca", TokenType.ROWS): [
                Entry(True, (TokenType.ROWS, "ROWS")), 
                Entry(False, "Caa")
            ],
            ("Caa", TokenType.FROM): [
                Entry(True, (TokenType.FROM, "FROM")), 
                Entry(False, "Caaa")
            ],
            ("Cb", TokenType.PLUS): [
                Entry(True, (TokenType.PLUS, "PLUS")), 
                Entry(False, "C")
            ],
            ("Cb", TokenType.FROM): [
                Entry(True, (TokenType.FROM, "FROM")), 
                Entry(False, "Cba")
            ],
            
            ("S", TokenType.IDENTIFIER): [
                Entry(True, (TokenType.IDENTIFIER, None)), 
                Entry(False, "X")
            ],
            ("X", TokenType.EQ): [
                Entry(True, (TokenType.EQ, "=")), 
                Entry(False, "S")
            ]
        }

        
    def peek(self):
        if self.current >= len(self.tokens):
            raise ParserError("Unexpected end of input")
        return self.tokens[self.current]
    
    def lookahead(self):
        if self.current + 1 >= len(self.tokens):
            raise ParserError("Unexpected end of input while looking ahead")
        return self.tokens[self.current + 1]
    
    def previous(self):
        if self.current <= 0:
            raise ParserError("Cannot get previous token at start of input")
        return self.tokens[self.current - 1]
    
    def advance(self):
        if self.current >= len(self.tokens) - 1:
            raise ParserError("Cannot advance past end of input")
        self.current += 1
    
    def match(self, tokenList):
        currentToken = self.peek()
        for token in tokenList:
            if currentToken[0] == token[0]:
                if token[1] is None or currentToken[1] == token[1]:
                    self.advance()
                    return True
        expected = ', '.join(f"{t[0]}({t[1]})" if t[1] else t[0] for t in tokenList)
        raise ParserError(f"Expected one of: {expected}, but got: {currentToken[0]}({currentToken[1]})", currentToken)
    
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


