import sys

from Exception import InvalidString, UnexpectedCharacter, InvalidSequence
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
        self.mod_stack = []
        self.raw_word = ""
        
        self.OP_TOKENS = {
          '=': 'EQ',
          '+': 'PLUS',
        }
        
        self.KEYWORDS = ['SHOW','FROM', 'LOAD','DATA', 'INTO', 'CONVERT', 'ROWS', 'COLUMNS', 'GET', 'IN', 'TO', 'OUTPUT', 'AS', 'GROUP_BY', 'PDF', 'CSV', 'JPEG']
        
        self.MODIFIERS = {
            ',': 'COMMA',
            '.': 'DOT',
            '(': 'LPAR',
            ')': 'RPAR',
        }
        
        
    def advance(self):
      self.current_position += 1
      if self.current_position >= len(self.current_line):
          self.current_char = None
      else:
          self.current_char = self.current_line[self.current_position]

    def find_next_break(self):
        index = self.current_line.find(' ', self.current_position)
        for modifier in self.MODIFIERS.keys():
            temp_index = self.current_line.find(modifier, self.current_position)
            if index != -1 and temp_index != -1:
                index = min(index, temp_index)
            if index == -1 and temp_index != -1:
                index = temp_index
        
        return index    
                
            
    def resolve_integer(self):
        num_str = ''
        while not (self.current_char.isspace() or self.current_char == ')'):
            
            if self.current_char.isalpha():
                next_break = self.find_next_break() 
                if next_break == -1:
                    # Pass the rest of the line
                    raise InvalidSequence(num_str+self.current_line[self.current_position: len(self.current_line)])
                else: 
                    raise InvalidSequence(num_str+self.current_line[self.current_position: next_break])

            num_str += self.current_char
            self.advance()

        
        return ('INTEGER', num_str)
    
    def keyword_or_identifier(self):
        if self.raw_word.upper() in self.KEYWORDS:
            self.line_tokens.append(('KEYWORD',self.raw_word.upper()))
            self.raw_word = ""
        else:
            self.line_tokens.append(('IDENTIFIER', self.raw_word))
            self.raw_word = ""
    
    def final_check(self):
        if len(self.mod_stack) > 0:
            mod = self.mod_stack.pop()
            raise InvalidString(f"{mod}{self.raw_word}")
        if len(self.mod_stack) == 0 and len(self.raw_word) > 0:
            self.keyword_or_identifier()
            
    def check_prev(self):
        truth = None
        if (self.prev_class == None or self.prev_class == "WHITESPACE" or self.prev_class == "OPERATOR"):
            truth = True
        else:
            truth = False
        return truth
    
    def valid_operator(self):
      return (self.current_position == len(self.current_line) - 1 or self.check_prev() or self.current_char == ")")
          
    def process_line(self):
        # Allows for line comments
        if "//" in self.current_line:
            return []
        
        while self.current_char is not None:
            if self.current_char.isspace():
                if len(self.raw_word) != 0:
                    self.keyword_or_identifier()
                    
                self.prev_class = 'WHITESPACE'
                self.line_tokens.append(('WHITESPACE',self.current_char))
                self.advance()
                continue
            
            # checking for identifier -- Second priority
            elif self.current_char.isalpha() or self.current_char == "_":
                    self.raw_word+=self.current_char
                    self.advance()
                    self.prev_class = "LITERAL"
                    continue
    
            # checking for operator
            elif self.current_char in self.OP_TOKENS and self.valid_operator():
                self.line_tokens.append((self.OP_TOKENS[self.current_char], self.current_char))
                self.prev_class = 'OPERATOR'
                self.advance()
                continue 
            
            # checking for modifier 
            elif self.current_char in self.MODIFIERS:
                if len(self.raw_word) != 0 and (self.current_char == "_" or self.current_char == "."):
                    self.raw_word += self.current_char
                    self.advance()
                    continue
                self.line_tokens.append((self.MODIFIERS[self.current_char], self.current_char))
                self.prev_class = 'MODIFIER'
                self.advance()
                continue 
            
            # checking for integer value 
            elif self.current_char.isdigit():
                if self.prev_class == "WHITESPACE" or self.prev_class == "MODIFIER":
                    self.line_tokens.append(self.resolve_integer())
                    self.prev_class = 'INTEGER'
                else:
                    self.prev_class = "LITERAL"
                    self.raw_word += self.current_char
                    
                self.advance()
                continue
            
            # parsing for strings
            elif self.current_char == '"' or self.current_char == "'":
                if len(self.mod_stack) == 0:
                    self.prev_class = "LITERAL"
                    self.mod_stack.append(self.current_char)
                else:
                    self.mod_stack.pop()
                    self.line_tokens.append(('STRING', self.raw_word))
                    self.prev_class = "STRING"
                    self.raw_word = ""              
                self.advance()  # Update the current character
            
            # doesn't matter what character, if it is in quotes it is fine
            elif len(self.mod_stack) >0: 
                self.raw_word += self.current_char
                self.advance()
            
            else:
                raise UnexpectedCharacter(self.current_char)
    
        self.final_check()
        return self.line_tokens
            
            
class CSVeaseLexer:
    def __init__(self,file):
        self.tokens = []
        self.file = file
        self.current_line_no = 0
        self.errors = LexerErrors(self.file)
      
    def resolve_tokens(self):
    # Open the file and ensure it's closed properly
        with open(self.file, "r") as file:
            for line in file:
                if len(line.strip()) == 0:
                    self.current_line_no += 1
                    continue
                try:
                    self.current_line_no += 1
                    line_to_process = Line(line)
                    self.tokens.extend(line_to_process.process_line())
                except UnexpectedCharacter as e:
                    self.errors.UnexpectedCharacter(line, self.current_line_no, e.error)
                except InvalidString as e:
                    self.errors.InvalidString(line, self.current_line_no, e.error)
                except InvalidSequence as e:
                    self.errors.InvalidSequence(line, self.current_line_no, e.error)
    
    def print_tokens(self):
        """
        count = {}
        for token in self.tokens:
            token_class, value = token
            if token_class not in count:
                count[token_class] = [token]
            else: 
                count[token_class].append(token)

        print(f"{len(self.tokens)} TOKENS: ")
        for key in count.keys():
            print(f"\n{key} ({len(count[key])})")
            if key == "WHITESPACE":
                print(f"    {count[key][0]}")
                print(f"            ...")
                print(f"    {count[key][0]}")
                continue
            for value in count[key]:
                token_class, token_val = value
                print(f"    <{token_class}, '{token_val}'>")
        """
        for token in self.tokens:
            token_class, token_val = token
            print(f"    <{token_class}, '{token_val}'>")
        

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