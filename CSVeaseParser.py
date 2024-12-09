import sys
from util_classes.ParserGrammar import ParserGrammar
from util_classes.Error import ParserError
from util_classes.Node import Node
from CSVeaseLexer import CSVeaseLexer

class CSVeaseParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.remove_white_space()
        self.current = 0
        self.stack = []
        self.buffer = []
        self.grammar = ParserGrammar()
        self.errors = []

    def remove_white_space(self):
        self.tokens = [t for t in self.tokens if t[0] != "WHITESPACE"]
        
    def peek(self):
        if self.current >= len(self.tokens):
            return ('$', '$')
        return self.tokens[self.current]
    
    def advance(self):
        self.current += 1


    def flatten_column_list(self, parse_node):
        if not parse_node:
            raise ParserError("Invalid parse node in column list")
        
        columns = []
    
        if parse_node.type == "IDENTIFIER":
            return [parse_node.value]
        
        elif parse_node.type in ["ColumnList", "ColumnListTail"]:
            for child in parse_node.children:
                if not child:
                    raise ParserError("Invalid child node in column list")
                if child.type == "IDENTIFIER":
                    columns.append(child.value)
                elif child.type == "ColumnListTail":
                    columns.extend(self.flatten_column_list(child))
        return columns

    def parse_tree_to_ast(self, parse_node):
        if not parse_node:
            raise ParserError("Invalid parse node in column list")
        
        if parse_node.type == "S":
            if not parse_node.children:
                raise ParserError("Root node has no children")
            return self.parse_tree_to_ast(parse_node.children[0])
        
        elif parse_node.type == "StmtList":
            statements = []
            # Handle the first statement
            if parse_node.children:
                stmt = self.parse_tree_to_ast(parse_node.children[0])
                statements.append(stmt)
                # If there's a StmtListTail, process it
                if len(parse_node.children) > 1:
                    tail_statements = self.parse_tree_to_ast(parse_node.children[1])
                    if isinstance(tail_statements, list):
                        statements.extend(tail_statements)
                    else:
                        statements.append(tail_statements)
            return Node("ProgramStart", children=statements)
        
        elif parse_node.type == "StmtListTail":
            statements = []
            if not parse_node.children:  # Empty tail (epsilon production)
                return statements
            # Process the statement
            stmt = self.parse_tree_to_ast(parse_node.children[0])
            statements.append(stmt)
            # Process the rest of the tail if it exists
            if len(parse_node.children) > 1:
                tail_statements = self.parse_tree_to_ast(parse_node.children[1])
                if isinstance(tail_statements, list):
                    statements.extend(tail_statements)
                else:
                    statements.append(tail_statements)
            return statements

        elif parse_node.type == "BaseStmt":
            if not parse_node.children:
                raise ParserError("BaseStmt has no children")
            return self.parse_tree_to_ast(parse_node.children[0])

        elif parse_node.type == 'AssignStmt':
            if len(parse_node.children) < 3:
                raise ParserError("AssignStmt has no children")
            return Node("Assign", children=[self.parse_tree_to_ast(child) 
                                        for child in parse_node.children if child.type not in ["EQ"]])
        
        elif parse_node.type == 'ConvertStmt':
            if len(parse_node.children) < 7:
                raise ParserError("Invalid CONVERT statement structure")
            return Node("Convert", children=[
                self.parse_tree_to_ast(parse_node.children[1]),
                self.parse_tree_to_ast(parse_node.children[3]),
                self.parse_tree_to_ast(parse_node.children[5]),
                self.parse_tree_to_ast(parse_node.children[6]),
            ])
            
        elif parse_node.type == 'LoadStmt':
            if len(parse_node.children) < 2:
                raise ParserError("LoadStmt has no children")
            return Node("Load", children=[self.parse_tree_to_ast(child) 
                                        for child in parse_node.children if child.type not in ["LOAD"]])

        elif parse_node.type == "GetStmt":
            if len(parse_node.children) < 4:
                raise ParserError("Invalid GET statement structure")
            columns = self.parse_tree_to_ast(parse_node.children[1])  
            from_identifier = parse_node.children[-1] 
            return Node("Get", children=[
                columns, 
                Node("Identifier", from_identifier.value)
            ])

        elif parse_node.type == "GetTarget":
            return Node("GetTarget", children=[self.parse_tree_to_ast(child) 
                                            for child in parse_node.children if child.type not in ["LPAREN", "RPAREN"]])

        elif parse_node.type == "ShowStmt":
            if len(parse_node.children) < 3:
                raise ParserError("ShowStmt has no children")
            show_type = parse_node.children[1].children[0].type
            identifier = parse_node.children[2].value
            return Node("Show", children=[
                Node("ShowType", show_type), 
                Node("Identifier", identifier)
            ])
            
        elif parse_node.type == "ColumnList":
            columns = self.flatten_column_list(parse_node)
            if not columns:
                raise ParserError("Empty column list")
            return Node("ColumnList", children=[Node("Identifier", col) for col in columns])
        
        elif parse_node.type == "IDENTIFIER":
            if not parse_node.value:
                raise ParserError("Identifier without value")
            return Node("Identifier", parse_node.value)

        elif parse_node.type == "STRING":
            if not parse_node.value:
                raise ParserError("String literal without value")
            return Node("String", parse_node.value)
        
        elif parse_node.type == 'OutputStmt':
            if len(parse_node.children) < 6:
                raise ParserError("Invalid OUTPUT statement structure")
            if parse_node.children[3].type != "STRING":
                raise ParserError("OUTPUT statement requires a string literal for file path")
            return Node("Output", children=[
                self.parse_tree_to_ast(parse_node.children[1]),  # IDENTIFIER
                self.parse_tree_to_ast(parse_node.children[3]),  # STRING
                self.parse_tree_to_ast(parse_node.children[5])   # FileType
            ])
        
        elif parse_node.type == 'DrawStmt':
            if len(parse_node.children) < 6:
                raise ParserError("Invalid DRAW statement structure")
            if parse_node.children[3].type != "STRING":
                raise ParserError("DRAW statement requires a string literal for file path")
            return Node("Draw", children=[
                self.parse_tree_to_ast(parse_node.children[1]),  # IDENTIFIER
                self.parse_tree_to_ast(parse_node.children[3]),  # STRING
                self.parse_tree_to_ast(parse_node.children[5])   # FileType
            ])
            
        elif parse_node.type == "FileType":
            if not parse_node.children:
                raise ParserError("FileType node has no children")
            # The first child will be CSV, JPEG, or PDF
            return Node("FileType", parse_node.children[0].type)
        
        elif parse_node.type == "ChartType":
            if not parse_node.children:
                raise ParserError("ChartType node has no children")
            # The first child will be CSV, JPEG, or PDF
            return Node("ChartType", parse_node.children[0].type)
        
        else:
            raise ParserError(f"Unknown node type: {parse_node.type}")
        
        
    def parse(self):
        root = Node('S')
        self.stack = [root, Node('$')]
        self.buffer = [('$', '$')] + self.tokens[::-1]
        
        try:
            while True:
                # Successful parse condition
                if (len(self.stack) == 1) and (self.stack[0].type == '$') and self.buffer == [('$','$')]:
                    return self.parse_tree_to_ast(root)
                    
                # Handle non-terminals
                elif self.stack[0].type not in self.grammar.terminals:
                    stack_head = self.stack[0]
                    non_term = stack_head.type
                    token = self.buffer[-1]
                    
                    production = self.grammar.parse_table.get((non_term, token[0]))
                    if production is None:  
                        raise ParserError(f"No production rule found for {non_term} with token {token[0]}")
                
                    if production == []:
                        stack_head.children = []
                        self.stack = self.stack[1:]
                        continue
                    # Create nodes from production and update stack
                    entry = self.parse_non_terminal(production)
                    stack_head.children = entry
                    self.stack = entry + self.stack[1:]
                    
                # Handle terminals
                else:
                    stack_head = self.stack[0]
                    token = self.buffer[-1]
                    
                    if stack_head.type != token[0]:
                        raise ParserError(f"Token mismatch: expected {stack_head.type}, got {token[0]}")
                        
                    stack_head.value = token[1]  # Store the actual value
                    self.stack = self.stack[1:]
                    self.buffer = self.buffer[:-1]
                    
        except Exception as e:
            raise(e)
    
    def parse_non_terminal(self, production):
        if not production:
            raise ParserError("Empty production rule")
        ret_list = []
        for p in production:
            ret_list.append(Node(p))
        return ret_list

    def format_ast(self,node, level=0):
        if not node:
            return ""
        result = "  " * level + str(node) + "\n"
        for child in node.children:
            result += self.format_ast(child, level + 1)
        return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]  
    else:
        print("Error: missing input file")
        exit()  # Correctly exit with parentheses
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    parser = CSVeaseParser(lexer.tokens)
    result = parser.parse()
    ast = parser.format_ast(result)
    print(ast)
    

    
    