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
        return self.ast

    def fold(self, node):
        if node.type == '+':
            node.type = 'String'
            node.value = node.children[0].value + node.children[1].value
            node.children = []
            return
        for child in node.children:
            self.fold(child)
        

class DeadCodeElimination:
    def __init__(self, ast):
        self.ast = ast
        self.used_variable = set()

    def run(self):
        self.eliminate(self.ast)
        return self.ast
    
    def eliminate(self, node):
        if node.type == "ProgramStart":
            live_children = []
            for child in reversed(node.children):
                if not self.eliminate(child):
                    live_children.append(child)
            node.children = list(reversed(live_children))
            return False
        
        elif node.type == 'Assign':
            id = node.children[0].value
            if id in self.used_variable:
                self.mark_used_variable(node.children[1])
                return False
            else:
                return True

        elif node.type == 'Identifier':
            self.used_variable.add(node.value)
            return False
        
        else:
            for child in node.children:
                self.eliminate(child)
            return False
        
    def mark_used_variable(self, node):
        if node.type == "Identifier":
            self.used_variable.add(node.value)
        elif node.children:
            for child in node.children:
               self.mark_used_variable(child)


class CommonSubExpressionElimination:
    def __init__(self, ast):
        self.ast = ast
        self.sub_expressions = {}

    def run(self):
        self.eliminate(self.ast)
        return self.ast
    
    def serialize(self, node):
        if not node.children:
            return f"{node.type}:{node.value}"
        return f"{node.type}({','.join(self.serialize(child) for child in node.children)})"

    def eliminate(self, node):
        if node.type == "ProgramStart":
            live_children = []
            for child in node.children:
                if child.type == 'Assign':
                    lhs = child.children[0]
                    rhs = child.children[1]
                    subtree_key = self.serialize(rhs)
                    if subtree_key in self.sub_expressions:
                        child.children = [lhs, self.sub_expressions[subtree_key]]
                    else:
                        self.sub_expressions[subtree_key] = lhs

                    live_children.append(child)
                else:
                    live_children.append(child)
            node.children = live_children
            



            


        


class CSVeaseOptimizer:
    def __init__(self, ast):
        self.ast = ast

    def optimize(self, technique):
        if technique == 'CommonSubExpressionElimination':
            cse = CommonSubExpressionElimination(self.ast)
            return cse.run()
        elif technique == 'ConstantFolding':
            cf = ConstantFolding(ast)
            return cf.run()
        elif technique == 'ConstantPropogation':
            cp = ConstantPropogation(ast)
            return cp.run()
        elif technique == 'DeadCodeElimination':
            dce = DeadCodeElimination(ast)
            return dce.run()
        else:
            return self.ast
        
    




if __name__ == "__main__":
    if len(sys.argv) > 1:
        file = sys.argv[1]
        technique = sys.argv[2]  
    else:
        print("Error: missing input file")
        exit()  # Correctly exit with parentheses
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    parser = CSVeaseParser(lexer.tokens)
    ast = parser.parse()
    try: 
        print("before optimization: ", technique)
        codegen = CSVeaseGenerator(ast)
        codegen.run()
    except Exception as e:
        print(e)
    try: 
        optimizer = CSVeaseOptimizer(ast)
        print("after optimization: ", technique)
        ast = optimizer.optimize(technique)
        codegen = CSVeaseGenerator(ast)
        codegen.run()
    except Exception as e:
        print(e)
    
    


    