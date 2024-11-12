class Node:
    def __init__(self, type: str, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []
    
    def __str__(self):
        if self.value and self.value != self.type:
            return f"{self.type}({self.value})"
        elif self.type in ['LPAREN', 'RPAREN', 'EQ', 'COMMA']:
            return self.type_to_symbol()
        return self.type
        
    def type_to_symbol(self):
        symbols = {
            'LPAREN': '(',
            'RPAREN': ')',
            'EQ': '=',
            'COMMA': ','
        }
        return symbols.get(self.type, self.type)
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        
        self.parse_table = {
            ('S', 'IDENTIFIER'): ['BaseStmt'],
            ('S', 'GET'): ['BaseStmt'],
            ('S', 'LOAD'): ['BaseStmt'],
            ('S', 'OUTPUT'): ['OutputStmt'],
            
            ('BaseStmt', 'IDENTIFIER'): ['AssignStmt'],
            ('BaseStmt', 'GET'): ['GetStmt'],
            ('BaseStmt', 'LOAD'): ['LoadStmt'],
            
            ('AssignStmt', 'IDENTIFIER'): ['IDENTIFIER', 'EQ', 'BaseStmt'],
            
            ('GetStmt', 'GET'): ['GET', 'GetTarget', 'FROM', 'B'],
            
            ('GetTarget', 'LPAREN'): ['ColumnList'],
            ('GetTarget', 'IDENTIFIER'): ['B'],
            
            ('ColumnList', 'LPAREN'): ['LPAREN', 'IdList', 'RPAREN'],
            
            ('IdList', 'IDENTIFIER'): ['IDENTIFIER', 'IdListTail'],
            
            ('IdListTail', 'COMMA'): ['COMMA', 'IDENTIFIER', 'IdListTail'],
            ('IdListTail', 'RPAREN'): [],  # ε production
            
            ('LoadStmt', 'LOAD'): ['LOAD', 'B'],
            
            ('OutputStmt', 'OUTPUT'): ['OUTPUT', 'B', 'TO', 'B', 'AS', 'FileType'],
            
            ('FileType', 'CSV'): ['CSV'],
            ('FileType', 'JPEG'): ['JPEG'],
            ('FileType', 'PDF'): ['PDF'],
            
            ('B', 'IDENTIFIER'): ['IDENTIFIER']
        }


    def build_id_list_tail_node(self, production):
        if not production:
            return None
            
        node = Node('ID_LIST')
        self.advance() 
        id_token = self.advance() 
        node.children.append(Node('IDENTIFIER', id_token[1]))
        
        next_token = self.peek()
        if next_token[0] == 'COMMA':
            tail_node = self.parse_non_terminal('IdListTail')
            if tail_node:
                node.children.extend(tail_node.children)
                        
        return node
    
    def peek(self):
        if self.current >= len(self.tokens):
            return ('$', '$')
        return self.tokens[self.current]
    
    def advance(self):
        token = self.peek()
        self.current += 1
        return token

    def parse(self):
        return self.parse_non_terminal('S')
    
    def parse_non_terminal(self, non_terminal):
        current_token = self.peek()
        production = self.parse_table.get((non_terminal, current_token[0]))
        
        if not production:
            raise Exception(f"No production found for {non_terminal} with token {current_token}")
        
        if non_terminal == 'S':
            return self.build_s_node(production)
        elif non_terminal == 'BaseStmt':
            return self.build_base_stmt_node(production)
        elif non_terminal == 'AssignStmt':
            return self.build_assign_stmt_node(production)
        elif non_terminal == 'GetStmt':
            return self.build_get_stmt_node(production)
        elif non_terminal == 'GetTarget':
            return self.build_get_target_node(production)
        elif non_terminal == 'ColumnList':
            return self.build_column_list_node(production)
        elif non_terminal == 'IdList':
            return self.build_id_list_node(production)
        elif non_terminal == 'IdListTail':
            return self.build_id_list_tail_node(production)
        elif non_terminal == 'LoadStmt':
            return self.build_load_stmt_node(production)
        elif non_terminal == 'OutputStmt':
            return self.build_output_stmt_node(production)
        elif non_terminal == 'FileType':
            return self.build_file_type_node(production)
        elif non_terminal == 'B':
            return self.build_b_node(production)
            
    def build_s_node(self, production):
        if production[0] == 'BaseStmt':
            return self.parse_non_terminal('BaseStmt')
        else:  
            return self.parse_non_terminal('OutputStmt')
            
    def build_base_stmt_node(self, production):
        if production[0] == 'AssignStmt':
            return self.parse_non_terminal('AssignStmt')
        elif production[0] == 'GetStmt':
            return self.parse_non_terminal('GetStmt')
        else:
            return self.parse_non_terminal('LoadStmt')
            
    def build_assign_stmt_node(self, production):
        node = Node('ASSIGN')
        id_token = self.advance() 
        node.children.append(Node('IDENTIFIER', id_token[1]))
        self.advance() 
        right_node = self.parse_non_terminal('BaseStmt')
        node.children.append(right_node)
        return node
            
    def build_get_stmt_node(self, production):
        node = Node('GET')
        self.advance() 
        target_node = self.parse_non_terminal('GetTarget')
        node.children.append(target_node)
        self.advance() 
        from_node = Node('FROM')
        b_node = self.parse_non_terminal('B')
        from_node.children.append(b_node)
        node.children.append(from_node)
        return node
    
    def build_get_target_node(self, production):
        if production[0] == 'ColumnList':
            return self.parse_non_terminal('ColumnList')
        else:  # B
            return self.parse_non_terminal('B')
    
    def build_column_list_node(self, production):
        node = Node('COLUMN_LIST')
        self.advance() 
        id_list_node = self.parse_non_terminal('IdList')
        node.children.append(id_list_node)
        self.advance()  
        return node
    
    def build_id_list_node(self, production):
        node = Node('ID_LIST')
        id_token = self.advance()  
        node.children.append(Node('IDENTIFIER', id_token[1]))
        tail_node = self.parse_non_terminal('IdListTail')
        if tail_node:
            node.children.extend(tail_node.children)
        return node
    
    def build_load_stmt_node(self, production):
        node = Node('LOAD')
        self.advance() 
        b_node = self.parse_non_terminal('B')
        node.children.append(b_node)
        return node
    
    def build_output_stmt_node(self, production):
        node = Node('OUTPUT')
        self.advance()  
        source_node = self.parse_non_terminal('B')
        node.children.append(source_node)
        self.advance() 
        
        dest_node = self.parse_non_terminal('B')
        node.children.append(dest_node)
        self.advance() 
        type_node = self.parse_non_terminal('FileType')
        node.children.append(type_node)
        return node
    
    def build_file_type_node(self, production):
        token = self.advance()
        return Node('FILE_TYPE', token[0])
    
    def build_b_node(self, production):
        id_token = self.advance()
        return Node('IDENTIFIER', id_token[1])

def print_ast(node, level=0):
    if not node:
        return ""
    result = " " * level + str(node) + "\n"
    for child in node.children:
        result += print_ast(child, level + 1)
    return result

if __name__ == "__main__":
    # tokens1 = [
    #     ('IDENTIFIER', 'table1'), ('EQ', '='), ('GET', 'GET'),
    #     ('LPAREN', '('), ('IDENTIFIER', 'col1'), ('COMMA', ','),
    #     ('IDENTIFIER', 'col2'), ('RPAREN', ')'),
    #     ('FROM', 'FROM'), ('IDENTIFIER', 'source_table')
    # ]
    
    tokens2 = [
        ('OUTPUT', 'OUTPUT'), ('IDENTIFIER', 'table1'),
        ('IDENTIFIER', 'output.csv'),
        ('AS', 'AS'), ('CSV', 'CSV')
    ]
    """
    parser = Parser(tokens1)
    ast = parser.parse()
    print("AST for Assignment + GET:")
    print(print_ast(ast))
    """
    
    parser = Parser(tokens2)
    ast = parser.parse()
    print("\nAST for OUTPUT:")
    print(print_ast(ast))