import sys
from CSVeaseLexer import CSVeaseLexer
from CSVeaseParser import CSVeaseParser
import os

class CSVeaseGenerator:
    def __init__(self, ast, file):
        self.ast = ast
        self.file = file
        # TODO: implement the to PDF functionality
        self.python_code = "import pandas as pd \nimport matplotlib.pyplot as plt\n"

    # TODO: export to temp python file and then actually execute it
    def run(self):
        res = self.generate(self.ast)
        try:
            exec(self.python_code + res)       
        except FileNotFoundError as e:
            print(f"CSVeaseGenerator: Could not find '{e.filename}'")
            print(os.getcwd())
            exit()
        except Exception as e:
            print(f"CSVeaseGenerator: {e.args}")
             
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
            xaxis = self.generate(node.children[2])
            yaxis = self.generate(node.children[3])
            return f"{identifier}.plot.{charttype}(x='{xaxis}', y='{yaxis}')"
        
        elif node.type == "Output":
            id = self.generate(node.children[0])
            file_name = self.generate(node.children[1])
            file_type = self.generate(node.children[2])
            return f"{id}.{file_type}({file_name})"
        
        elif node.type == "Draw":
            id = self.generate(node.children[0])
            file_name = self.generate(node.children[1])
            file_type = self.generate(node.children[2])
            return f"""plt.savefig({file_name}, format="{file_type}")"""
        
        elif node.type == 'FileType':
            if node.value == 'CSV':
                return "to_csv"
            elif node.value == 'JPEG':
                return "jpeg"
            elif node.value == 'PDF':
                return "pdf"
            
        elif node.type == 'ChartType':
            if node.value == 'BARCHART':
                return "bar"

if __name__ == "__main__":

    if len(sys.argv) > 1:
        file = sys.argv[1]  
    else:
        print("Error: missing input file")
        exit()
        
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    if lexer.errors.error_count > 0:
        lexer.errors.printErrors()
        exit()
    try:
        parser = CSVeaseParser(lexer.tokens)
        result = parser.parse()
    except Exception as e:
        print(f"CSVeaseParser: {e}")
        exit()
    
    try:    
        codegen = CSVeaseGenerator(result, file)
        codegen.run()
    except Exception as e:
        pass