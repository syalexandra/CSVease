import sys

from Exception import BadIdentifier, UnexpectedCharacter

# TODO: do the error handling @ Phillip
# identifier, but the id starts with a number -> throw an error
# 
# Use the stack to ensure that there are matching sets 
class LexerDFA:
    def __init__(self,input_string):
        self.tokens = []
        self.current_position = 0
        self.end_position = self.current_position
        self.current_char = input_string[self.current_position] if input_string else None
        self.input_string = input_string


    def advance(self):
        self.current_position += 1
        self.end_position = self.current_position
        if self.current_position >= len(self.input_string):
            self.current_char = None
        else:
            self.current_char = self.input_string[self.current_position]

    def retreat(self):
        self.current_position -= 1
        self.end_position = self.current_position
        if self.current_position <= 0:
            self.current_char = None
        else:
            self.current_char = self.input_string[self.current_position]
            
    def matchKeyWord(self,start,length,targetString):
        if self.input_string[start:start+length] == targetString:
            return start+length
        else:
            return start

    def isKeyword(self):
        if self.current_char == 'S':
            self.end_position = self.matchKeyWord(self.current_position,4,"SHOW")
            if self.end_position > self.current_position:
                return True
            else:
                return False
        elif self.current_char == 'I':
            self.end_position = self.matchKeyWord(self.current_position,2,"IN")
            if self.end_position > self.current_position:
                return True
            else:
                return False
        else:
            return False
        
    def findEndOfIdentifier(self):
        while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
            self.end_position += 1
            if self.end_position >= len(self.input_string):
                self.current_char = None
                return self.end_position
            else:
                self.current_char = self.input_string[self.end_position]
        if self.current_char.isspace() or self.current_char == ')':
            return self.end_position
        else:
            raise BadIdentifier
        
        
    def resolve_integer(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        # test to see if the next character is a space
        self.advance()
        if self.current_char.isspace() or self.current_char == ')':
            self.retreat()
            return ('INTEGER', num_str)           
        # In the case where the input is 123+ or 123abc 
        else:
            self.retreat()
            raise BadIdentifier

    def run(self):
        while self.current_char is not None:
            if self.current_char == ',':
                self.tokens.append(('COMMA',','))
                self.advance()

            elif self.current_char == '.':
                self.tokens.append(('DOT','.'))
                self.advance()
            
            elif self.current_char == '=':
                self.tokens.append(('EQ','='))
                self.advance()
            
            elif self.current_char == '+':
                self.tokens.append(('PLUS','+'))
                self.advance()

            elif self.current_char == '(':
                self.tokens.append(('LPAR','('))
                self.advance()
            
            elif self.current_char == ')':
                self.tokens.append(('RPAR',')'))
                self.advance()

            elif self.current_char.isspace():
                self.tokens.append(('WHITESPACE',self.current_char))
                self.advance()

            elif self.current_char.isdigit():
                self.tokens.append(self.resolve_integer())
                self.advance()

            elif self.current_char.isalpha():
                if self.isKeyword():
                    self.tokens.append(('KEYWORD',self.input_string[self.current_position:self.end_position]))
                    self.current_position = self.end_position
                    if self.current_position >= len(self.input_string):
                        self.current_char = None
                    else:
                        self.current_char = self.input_string[self.current_position]
                else:
                    self.end_position = self.findEndOfIdentifier()
                    self.tokens.append(('IDENTIFIER',self.input_string[self.current_position:self.end_position]))
                    self.current_position = self.end_position
                    if self.current_position >= len(self.input_string):
                        self.current_char = None
                    else:
                        self.current_char = self.input_string[self.current_position]
            else: 
                raise UnexpectedCharacter(self.current_char)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_string = sys.argv[1]  
    else:
        input_string = ''
    
    lexer = LexerDFA(input_string)
    try:
        lexer.run()
        print(lexer.tokens)
    except Exception as e:
        print(e)
    
    
# <IDENTIGIER, >
# // this will load a csv file and create an instance of the csv file as table2 

# table1 = load class_roster.csv

# // output rows and columns

# show rows table1
# show columns	table1

# // select function

# sub_table = get (NAME, AGE, YEAR) IN table1

# // selecting the year column, getting the average age of each year in the table and creating a new group table -> example below

# group_table = avg(age) group by (YEAR) IN sub_table

# // creates a new csv file called group_table.csv with those changes
# chart1 = convert group_table to bar chart


# output group_table TO group_table_file as CSV 
# output group_table TO group_table_file as PDF
# output group_table TO chart1 as JPEG 
