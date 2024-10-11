import sys

from Exception import InvalidString, LexerErrors, BadIdentifier, UnexpectedCharacter, InvalidSequence
from Error import LexerErrors

# TODO: do the error handling @ Phillip
# identifier, but the id starts with a number -> throw an error
# 
# Use the stack to ensure that there are matching sets 

class Line:
  
    def __init__(self, line):
        self.line_tokens = []
        self.current_line = line.strip()
        self.current_position = 0
        self.current_char = self.current_line[self.current_position] if self.current_line else None
        self.prev_class = None
        self.OP_TOKENS = {
          '=': 'EQ',
          '+': 'PLUS',
          '(': 'LPAR',
          ')': 'RPAR',
        }
        self.KEYWORDS = ['SHOW', 'LOAD', 'CONVERT', 'ROWS', 'COLUMNS', 'GET', 'IN', 'TO', 'OUTPUT', 'AS', 'PDF', 'CSV', 'JPEG']
        self.MODIFIERS = {
            ',': 'COMMA',
            '.': 'DOT',
        }
        
    def advance(self):
      self.current_position += 1
      if self.current_position >= len(self.current_line):
          self.current_char = None
      else:
          self.current_char = self.current_line[self.current_position]

    def retreat(self):
        self.current_position -= 1
        if self.current_position <= 0:
            self.current_char = None
        else:
            self.current_char = self.current_line[self.current_position]
            
    def matchKeyWord(self,start,length,targetString):
        if self.current_line[start:start+length] == targetString:
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
        
    def resolve_integer(self):
        num_str = ''
        while  self.current_char is not None:
            # We reached the end of the sequence and we want to return the integer
            if self.current_char.isspace() or self.current_char == ')':
                self.advance()
                return ('INTEGER', num_str)           
            if self.current_char.isalpha():
                raise InvalidSequence(self.current_line)
            num_str += self.current_char
            self.advance()
          
    def check_prev(self):
      return (self.prev_class == None or self.prev_class == "WHITESPACE" or self.prev_class == "OPERATOR")
    
    def valid_operator(self):
      if self.current_position == len(self.current_line) - 1 or self.check_prev() or self.current_char == ")":
          return True
                
      return False
    def find_next_index(self):
        next_index =  self.current_line.find(' ', self.current_position)
        
        for operator in self.OP_TOKENS.keys():
            test_index = self.current_line.find(operator, self.current_position)
            if test_index == -1: 
                continue
            else:
                if next_index != -1:
                    next_index = min(test_index, next_index)
        
        for modifider in self.MODIFIERS.keys():
            test_index = self.current_line.find(modifider, self.current_position)
            if test_index == -1: 
                continue
            else:
                if next_index != -1:
                    next_index = min(test_index, next_index)
                    
        return next_index
          
    def process_line(self):
        while self.current_char is not None:
            next_space = self.find_next_index()
            if next_space == -1:  # No more spaces found
                unit = self.current_line[self.current_position:]  # Take the rest of the line
            else:
                unit = self.current_line[self.current_position: next_space]  
                            
            if self.current_char.isspace():
                self.prev_class = 'WHITESPACE'
                self.line_tokens.append(('WHITESPACE',self.current_char))
                self.advance()
                continue
            
            # checking for keyword -- Highest priority
            if unit.upper() in self.KEYWORDS and self.check_prev():
                self.line_tokens.append(('KEYWORD',unit.upper()))
                self.current_position = self.current_line.find(' ', self.current_position)
                if self.current_position >= len(self.current_line) or self.current_position == -1:
                    self.current_char = None
                else:
                    self.prev_class = 'KEYWORD'
                    self.current_char = self.current_line[self.current_position]
                continue 
              
            # checking for identifier -- Second priority
            elif self.current_char.isalpha() and self.check_prev():
              self.line_tokens.append(('IDENTIFIER', unit))
              self.current_position = next_space
              if self.current_position >= len(self.current_line) or self.current_position == -1:
                  self.current_char = None
              else:
                  self.prev_class = 'IDENTIFIER'
                  self.current_char = self.current_line[self.current_position]
              continue
            
            # checking for operator
            elif self.current_char in self.OP_TOKENS and self.valid_operator():
                self.line_tokens.append((self.OP_TOKENS[self.current_char], self.current_char))
                self.prev_class = 'OPERATOR'
                self.advance()
                continue 
            
            elif self.current_char in self.MODIFIERS:
                self.line_tokens.append((self.MODIFIERS[self.current_char], self.current_char))
                self.prev_class = 'MODIFIER'
                self.advance()
                continue 
            
            # checking for integer value 
            elif self.current_char.isdigit():
                self.line_tokens.append(self.resolve_integer())
                self.prev_class = 'INTEGER'
                self.advance()
                continue
            
            # parsing for strings
            elif self.current_char == '"':
                next_quot = self.current_line.find('"', self.current_position + 1)  # Start searching from next position
                if next_quot == -1:  # No closing quote found
                    raise InvalidString(f"No closing quote found for string starting at position {self.current_position}")
                string_value = self.current_line[self.current_position + 1: next_quot]  # Exclude the quotes
                self.line_tokens.append(('STRING', string_value))
                self.current_position = next_quot + 1  # Move past the closing quote
                self.advance()  # Update the current character
                continue
            else: 
                raise UnexpectedCharacter
          
        return self.line_tokens
            
            
class CSVeaseLexer:
    def __init__(self,file):
        self.tokens = []
        self.file = file
        self.current_line_no = 0
        self.errors = LexerErrors()
      
    def resolve_tokens(self):
    # Open the file and ensure it's closed properly
        with open(self.file, "r") as file:
            for line in file:
                if len(line.strip()) == 0:
                    continue
                try:
                    self.current_line_no += 1
                    line_to_process = Line(line)
                    self.tokens.extend(line_to_process.process_line())
                except UnexpectedCharacter as e:
                    self.errors.UnexpectedCharacter(line, self.current_line_no)
                except BadIdentifier as e:
                    self.errors.BadIdentifier(line, self.current_line_no)
                except InvalidString as e:
                    self.errors.InvalidString(line, self.current_line_no)
                except InvalidSequence as e:
                    self.errors.InvalidSequence(line, self.current_line_no)
    
    def print_tokens(self):
      for token in self.tokens:
        token_class, value = token
        if token_class == "WHITESPACE":
            continue
        print(f"<{token_class}, '{value}'>")
        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]  
    else:
        print("Error: missing input file")
        exit()  # Correctly exit with parentheses
    
    lexer = CSVeaseLexer(file)
    lexer.resolve_tokens()
    if lexer.errors.error_count > 0:
        lexer.errors.printErrors()
    else:
        lexer.print_tokens()
    
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
