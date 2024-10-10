token_types = (
    'IDENTIFIER',
    'PLUS',
    'INTEGER',
    'STRING',
    'KEYWORD',
    'WHITESPACE',# should we ignore whitespace?
    'LPAR',
    'RPAR',
    'COMMA'
    'DOT',

)

reserved_keywords = (
    'SHOW',
    'IN',
    'ROWS',
    'COLUMNS',
    'LOAD',
    'AS',
    'GET',
    'AVG'
)



class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

