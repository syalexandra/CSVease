import sys
from util_classes.ParserGrammar import ParserGrammar
from util_classes.Error import ParserError
from util_classes.Node import Node
from CSVeaseLexer import CSVeaseLexer
from CSVeaseParser import CSVeaseParser
from CSVeaseGenerator import CSVeaseGenerator

class ConstantPropogation:
    def __init__(self, ast):
        self.ast = ast
        self.constantTable = {}

    def run(self):
        self.propogate(self.ast)
        return self.ast

    def propogate(self, node):
        if node.type == "Assign":
            firstchild = node.children[0]
            secondchild = node.children[1]
            if firstchild.type == 'Identifier' and secondchild.type in ['String']:
                self.constantTable[(firstchild.type, firstchild.value)] = (secondchild.type, secondchild.value)
                return

        elif node.type == "Identifier":
            if (node.type, node.value) in self.constantTable:
                v = self.constantTable[(node.type, node.value)]
                node.type, node.value = v
                return
        for child in node.children:
            self.propogate(child)



class ConstantFolding:
    def __init__(self, ast):
        self.ast = ast
    
    def run(self):
        self.fold(self.ast)

    def fold(self, node):
        return
"""
class CSVeaseOptimizer:
    def __init__(self, ast):
        self.ast = ast
"""



if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]  
    else:
        print("Error: missing input file")
        exit()  # Correctly exit with parentheses
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    parser = CSVeaseParser(lexer.tokens)
    ast = parser.parse()
    cp = ConstantPropogation(ast)
    ast = cp.run()
    codegen = CSVeaseGenerator(ast, '')
    codegen.run()

    