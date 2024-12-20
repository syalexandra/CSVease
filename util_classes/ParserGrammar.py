class ParserGrammar:
    def __init__(self):
        self._init_terminals()
        self._init_parse_table()
    
    def _init_terminals(self):
        self.terminals = [
            'IDENTIFIER', 'SHOW', 'GET', 'LOAD', 'INTO', 'FROM', 'TO', 'OUTPUT',
            'ROWS', 'COLUMNS', 'LPAREN', 'COMMA', 'RPAREN', 'LPAR', 'RPAR',
            'OUTPUT', 'CSV', 'JPEG', 'PDF', 'EQ', 'PLUS', 'AS', 'STRING',
            'IN', 'AVG', 'GROUP_BY', 'CONVERT', 'BARCHART','WITH','DRAW'
        ]
    
    def _init_parse_table(self):
        self.parse_table = {
            ('S', 'IDENTIFIER'): ['StmtList'],
            ('S', 'GET'): ['StmtList'],
            ('S', 'LOAD'): ['StmtList'],
            ('S', 'OUTPUT'): ['StmtList'],
            ('S', 'DRAW'): ['StmtList'],
            ('S', 'SHOW'): ['StmtList'],
            ('S', 'CONVERT'): ['StmtList'],

            ('StmtList', 'IDENTIFIER'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'GET'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'LOAD'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'OUTPUT'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'DRAW'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'SHOW'): ['BaseStmt', 'StmtListTail'],
            ('StmtList', 'CONVERT'): ['BaseStmt', 'StmtListTail'],

            ('StmtListTail', 'IDENTIFIER'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', 'GET'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', 'LOAD'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', 'OUTPUT'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', 'SHOW'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', 'DRAW'): ['BaseStmt', 'StmtListTail'],
            ('StmtListTail', '$'): [],  
            
            ('BaseStmt', 'IDENTIFIER'): ['AssignStmt'],
            ('BaseStmt', 'CONVERT'): ['ConvertStmt'],
            ('BaseStmt', 'GET'): ['GetStmt'],
            ('BaseStmt', 'LOAD'): ['LoadStmt'],
            ('BaseStmt', 'SHOW'): ['ShowStmt'],
            ('BaseStmt', 'OUTPUT'): ['OutputStmt'],
            ('BaseStmt', 'DRAW'): ['DrawStmt'],
            ('BaseStmt', 'STRING'):['STRING', 'StrStmt'],
            
            ('AssignStmt', 'IDENTIFIER'): ['IDENTIFIER', 'EQ', 'BaseStmt'],
            ('ConvertStmt', 'CONVERT'): ['CONVERT', 'IDENTIFIER', 'TO', 'ChartType','WITH','IDENTIFIER','IDENTIFIER'],
            ('GetStmt', 'GET'): ['GET', 'GetTarget', 'FROM', 'IDENTIFIER'],
            ('StrStmt', 'PLUS'):['PLUS', 'STRING'],
            ('StrStmt', 'IDENTIFIER'):[],
            ('StrStmt', '$'):[],

            
            ('GetTarget', 'LPAREN'): ['LPAREN','ColumnList', 'RPAREN'],
            ('GetTarget', 'IDENTIFIER'): ['IDENTIFIER'],
            ('ColumnList', 'IDENTIFIER'): ['IDENTIFIER', 'ColumnListTail'],
            ('ColumnListTail', 'COMMA'): ['COMMA', 'IDENTIFIER', 'ColumnListTail'],
            ('ColumnListTail', 'RPAREN'): [], 
            
            ('LoadStmt', 'LOAD'): ['LOAD', 'LoadOptions'],
            ('LoadOptions', 'STRING'):['STRING'],
            ('LoadOptions', 'IDENTIFIER'):['IDENTIFIER'],
            
            ('OutputStmt', 'OUTPUT'): ['OUTPUT', 'IDENTIFIER', 'TO', 'STRING', 'AS', 'FileType'],
            ('DrawStmt', 'DRAW'): ['DRAW', 'IDENTIFIER', 'TO', 'STRING', 'AS', 'FileType'],
            ('ShowStmt', 'SHOW'): ['SHOW', 'ShowOptions', 'IDENTIFIER'],
            ('ShowOptions', 'ROWS'): ['ROWS'],
            ('ShowOptions', 'COLUMNS'): ['COLUMNS'],
            ('FileType', 'CSV'): ['CSV'],
            ('FileType', 'JPEG'): ['JPEG'],
            ('FileType', 'PDF'): ['PDF'],
            ('ChartType', 'BARCHART'): ['BARCHART']
        }
        