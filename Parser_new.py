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
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.stack = []
        self.buffer = []
        self.terminals = ['IDENTIFIER', 'GET', 'LOAD', 'INTO', 'FROM', 'TO', 'OUTPUT', 'LPAREN', 'COMMA', 'RPAREN',
                          'OUTPUT', 'CSV', 'JPEG', 'PDF', 'EQ', 'PLUS', 'AS' , 'STRING']
        
        self.parse_table = {
            ('S', 'IDENTIFIER'): ['BaseStmt'],
            ('S', 'GET'): ['BaseStmt'],
            ('S', 'LOAD'): ['BaseStmt'],
            ('S', 'OUTPUT'): ['OutputStmt'],
            
            ('BaseStmt', 'IDENTIFIER'): ['AssignStmt'],
            ('BaseStmt', 'GET'): ['GetStmt'],
            ('BaseStmt', 'LOAD'): ['LoadStmt'],
            
            ('AssignStmt', 'IDENTIFIER'): ['IDENTIFIER', 'EQ', 'BaseStmt'],
            
            ('GetStmt', 'GET'): ['GET', 'GetTarget', 'FROM', 'IDENTIFIER'],
            
            ('GetTarget', 'LPAREN'): ['LPAREN','ColumnList', 'RPAREN'],
            ('GetTarget', 'IDENTIFIER'): ['IDENTIFIER'],
            ('ColumnList', 'IDENTIFIER'): ['IDENTIFIER', 'ColumnListTail'],
            ('ColumnListTail', 'COMMA'): ['COMMA', 'IDENTIFIER', 'ColumnListTail'],
            ('ColumnListTail', 'RPAREN'): [],  # ε production
            
            #('ColumnSingle', 'IDENTIFIER'):['IDENTIFIER', 'ColumnSingleTail'],
            #('ColumnSingleTail', 'PLUS'): ['PLUS', 'IDENTIFIER', 'ColumnSingleTail'],
            #('ColumnList', 'IDENTIFIER'): ['ColumnListItem', 'ColumnListTail'],
            #('ColumnListItem', 'IDENTIFIER'): ['IDENTIFIER', 'ColumnListItemTail'],
            #('ColumnListItemTail', 'PLUS'): ['PLUS', 'IDENTIFIER', 'ColumnListItemTail'],
            #('ColumnListItemTail', 'RPAREN'): [],
            #('ColumnListItemTail', 'COMMA'): [],
            #('ColumnListTail', 'COMMA'): ['COMMA', 'ColumnListItem', 'ColumnListTail'],
            #('ColumnListTail', 'RPAREN'): [],  # ε production

            
            ('LoadStmt', 'LOAD'): ['LOAD', 'STRING'],
            
            ('OutputStmt', 'OUTPUT'): ['OUTPUT', 'IDENTIFIER', 'TO', 'STRING', 'AS', 'FileType'],
            
            ('FileType', 'CSV'): ['CSV'],
            ('FileType', 'JPEG'): ['JPEG'],
            ('FileType', 'PDF'): ['PDF'],
        }

    
    def peek(self):
        if self.current >= len(self.tokens):
            return ('$', '$')
        return self.tokens[self.current]
    
    def advance(self):
        self.current += 1


    def flatten_column_list(self, parse_node):
        columns = []
    
        # Base case: if the node is an identifier, add it to the list
        if parse_node.type == "IDENTIFIER":
            return [parse_node.value]
        
        # If the node is ColumnList or ColumnListTail, process its children
        elif parse_node.type in ["ColumnList", "ColumnListTail"]:
            for child in parse_node.children:
                if child.type == "IDENTIFIER":
                    # Add identifier directly
                    columns.append(child.value)
                elif child.type == "ColumnListTail":
                    # Recursively flatten ColumnListTail
                    columns.extend(self.flatten_column_list(child))
                # Skip non-essential nodes like commas
        return columns

    def parse_tree_to_ast(self, parse_node):
        # If the node is a For Statement, we want to keep it in the AST
        if parse_node.type == "S":
            # Root of the program
            return self.parse_tree_to_ast(parse_node.children[0])
        
        elif parse_node.type == "BaseStmt":
            # Base statements are kept, but we only want their essential children
            return self.parse_tree_to_ast(parse_node.children[0])
    
        elif parse_node.type == 'AssignStmt':
            return Node("Assign", children=[self.parse_tree_to_ast(child) for child in parse_node.children if child.type not in ["EQ"]])
        
        elif parse_node.type == 'LoadStmt':
            return Node("Load", children=[self.parse_tree_to_ast(child) for child in parse_node.children if child.type not in ["LOAD"]])


        elif parse_node.type == "GetStmt":
            # For a GET statement, transform its important parts
            get_target = self.parse_tree_to_ast(parse_node.children[1])  # GetTarget child
            from_identifier = parse_node.children[-1]  # IDENTIFIER child
            return Node("GetStmt", children=[
                Node("Get", "GET"),
                get_target,
                Node("From", "FROM"),
                Node("Identifier", from_identifier.value)
            ])

        elif parse_node.type == "GetTarget":
            # Simplify GetTarget to directly store columns as children
            return Node("GetTarget", children=[self.parse_tree_to_ast(child) for child in parse_node.children if child.type not in ["LPAREN", "RPAREN"]])

        elif parse_node.type == "ColumnList":
            # Combine ColumnList and its items into a single structure
            columns = self.flatten_column_list(parse_node)
            return Node("ColumnList", children=[Node("Variable", col) for col in columns])
        
        elif parse_node.type == "IDENTIFIER":
            # Convert IDENTIFIER nodes to a simple Variable node
            return Node("Variable", parse_node.value)

        elif parse_node.type == "STRING":
            # Convert constants directly to their values
            return Node("String", parse_node.value)
        
        elif parse_node.type == 'OutputStmt':
            return Node("Output", children=[self.parse_tree_to_ast(child) for child in parse_node.children if child.type not in ["OUTPUT", "TO", "AS"]])

    def parse(self):
        root = Node('S')
        self.stack = [root, Node('$')]
        self.buffer = [('$', '$')] + self.tokens[::-1]
        prev_node = root
        while True:
            if (len(self.stack) ==1) and (self.stack[0].type =='$') and self.buffer == [('$','$')]:
                return self.parse_tree_to_ast(root)
            elif self.stack[0].type not in self.terminals:
                stack_head = self.stack[0]
                non_term = stack_head.type
                token = self.buffer[-1]
                try:
                    production = self.parse_table.get((non_term, token[0]))
                    entry = self.parse_non_terminal(production) #list of nodes
                    stack_head.children = entry
                    self.stack = entry + self.stack[1:]
                except:
                    raise Exception("invalid input")
            else:
                stack_head = self.stack[0]
                token = self.buffer[-1]
                if stack_head.type != token[0]:
                    raise Exception("invalid input")
                stack_head.value = token[-1]
                self.stack = self.stack[1:]
                self.buffer = self.buffer[:-1]

    
    def parse_non_terminal(self, production):
        ret_list = []
        for p in production:
            ret_list.append(Node(p))
        return ret_list

def print_ast(node, level=0):
    if not node:
        return ""
    result = " " * level + str(node) + "\n"
    for child in node.children:
        result += print_ast(child, level + 1)
    return result




    # Add other cases as necessary

    # Return None if the node doesn't fit into our AST structure
    return None

if __name__ == "__main__":
    token1 = [
        ('IDENTIFIER', 'table1'), ('EQ', '='), ('GET', 'GET'),
        ('LPAREN', '('), ('IDENTIFIER', 'col1'), ('COMMA', ','),
        ('IDENTIFIER', 'col2'), ('COMMA', ','),('IDENTIFIER', 'col3'),
        ('RPAREN', ')'),
        ('FROM', 'FROM'), ('IDENTIFIER', 'source_table')
    ]
    parser = Parser(token1)
    ast = parser.parse()
    print("AST for Assignment + GET:")
    print(print_ast(ast))
    
    
    token2 = [
        ('OUTPUT', 'OUTPUT'), ('IDENTIFIER', 'table1'),
        ('TO', 'TO'), ('STRING', 'output.csv'),
        ('AS', 'AS'), ('CSV', 'CSV')
    ]
    parser = Parser(token2)
    ast = parser.parse()
    print("\nAST for OUTPUT:")
    print(print_ast(ast))

    token3 = [
        ('IDENTIFIER', 'table1'), ('EQ', '='), 
        ('LOAD', 'LOAD'), ('STRING','file.csv')
    ]
    parser = Parser(token3)
    ast = parser.parse()
    print("\nAST for OUTPUT:")
    print(print_ast(ast))

    token4 = [
        ('IDENTIFIER', 'table1'), ('EQ', '='), 
        ('LOAD', 'LOAD'), ('IDENTIFIER','file')
    ]
    #this should throw error
    parser = Parser(token4)
    ast = parser.parse()
    print("\nAST for OUTPUT:")
    print(print_ast(ast))
    

    #this is a more complicated example, i haven't figured it out yet.
    token5 = [
        ('IDENTIFIER', 'table1'), ('EQ', '='), ('GET', 'GET'),
        ('LPAREN', '('), ('IDENTIFIER', 'col1'), ('PLUS','PLUS'), ('IDENTIFIER', 'col2'),('COMMA', ','),
        ('IDENTIFIER', 'col3'), ('RPAREN', ')'),
        ('FROM', 'FROM'), ('IDENTIFIER', 'source_table')
    ]
    
    