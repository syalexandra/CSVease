import sys
from util_classes.ParserGrammar import ParserGrammar
from util_classes.Error import ParserError
from util_classes.Node import Node
from CSVeaseLexer import CSVeaseLexer
from CSVeaseParser import CSVeaseParser

class CSVeaseOptimizer:
    def __init__(self, ast):
        self.ast = ast



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
    print(result)