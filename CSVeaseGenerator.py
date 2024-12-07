import sys
from CSVeaseLexer import CSVeaseLexer
from CSVeaseParser import CSVeaseParser

class CSVeaseGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.python_code = "import pandas as pd \n"

    def run(self):
        res = self.generate(self.ast)
        print(self.python_code + res)
        

    def generate(self, node):
        if node.type == 'ProgramStart':
            return "\n".join([self.generate(n) for n in node.children])

        elif node.type == 'Assign':
           return f"{self.generate(node.children[0])} = {self.generate(node.children[1])}"

        elif node.type == 'Load':
            return f"pd.read_csv({self.generate(node.children[0])})"

        elif node.type == 'String':
            return f'"{node.value}"'

        elif node.type == 'Show':
            showtype = node.children[0]
            identifier = node.children[1]
            return f"print({self.generate(identifier)}{self.generate(showtype)})"

        elif node.type == 'ShowType':
            if node.value == 'ROWS':
                return ".values.tolist()"
            elif node.value == 'COLUMNS':
                return ".columns.tolist()"
            
        elif node.type == 'Identifier':
            return node.value
        
        elif node.type == 'Get':
            target = node.children[0]
            identifier = node.children[1]
            return f"{self.generate(identifier)}[{self.generate(target)}]"

        elif node.type == 'GetTarget':
            return self.generate(node.children[0])
        
        elif node.type == 'ColumnList':
            columns = "','".join([self.generate(i) for i in node.children])
            return f"['{columns}']"
        
        elif node.type == 'Convert':
            #this needs more details
            identifier = self.generate(node.children[0])
            charttype = self.generate(node.children[1])
            return ""
        
        elif node.type == "Output":
            id = self.generate(node.children[0])
            file_name = self.generate(node.children[1])
            file_type = self.generate(node.children[2])
            return f"{id}.{file_type}({file_name})"
        
        elif node.type == 'FileType':
            if node.value == 'CSV':
                return "to_csv"
            
            ## note: output a dataset to pdf / csv is difficult, change to excel instead
            
            




if __name__ == "__main__":
    """
    if len(sys.argv) > 1:
        file = sys.argv[1]  
    else:
        print("Error: missing input file")
        exit()  # Correctly exit with parentheses
    """
    file = "input/original.ease"
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    parser = CSVeaseParser(lexer.tokens)
    result = parser.parse()
    codegen = CSVeaseGenerator(result)
    codegen.run()