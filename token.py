token_types = (
    'IDENTIFIER',
    'PLUS',
    'INTEGER',
    'STRING',
    'KEYWORD',
    'WHITESPACE',
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
"abc"


class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

