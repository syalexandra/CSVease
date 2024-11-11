# CSVease Lexer
Developers: Phillip Le (pnl2111) and Yue Sun (ys3535)

## Lexical Grammar Rules (Descending Priority)
### 1. Strings
- Characterized by the following format "[any character]" or '[any character]'
### 2. Whitespace 
### 3. Keywords and Identifiers
- Identifiers must **not** start with a digit.
- Identifiers can include:
  - Letters (A-Z, a-z)
  - Digits (0-9), but **not** as the first character
  - Underscores (`_`)
- KEYWORDS = ['SHOW','FROM', 'LOAD','DATA', 'INTO', 'CONVERT', 'ROWS', 'COLUMNS', 'GET', 'IN', 'TO', 'OUTPUT', 'AS', 'GROUP_BY', 'PDF', 'CSV', 'JPEG','AVG','BAR','CHART']

4. Operators 
- "+" and "="
5. Modifiers
- MODIFIERS = {
            ',': 'COMMA',
            '.': 'DOT',
            '(': 'LPAR',
            ')': 'RPAR',
        }
6. Integers 
7. Unexpected Characters
- In the case where the above rules do not apply and we are not parsing a string.

## Error Handling in CSVease
We have developed different exceptions and errors for our lexer. The lexer will read the input file line by line and process each line sequentially. In the case where there is an error in the input file, we throw an exception but we catch exception and add the neccessary logging into an array such that we still process the rest of the file. **However, if there were errors present, then the lexer will print the errors and not return the tokens.**

### Exceptions and Errors:
1. InvalidSequence
2. UnexpectedCharacter
3. InvalidString


## Tokens
<KEYWORD, 'keyword'>\
<IDENTIFIER, 'identifier'>\
<INTEGER, '4115'>\
<WHITESPACE, ' '>\
<STRING, 'string'>\
<COMMA, ','>\
<LPAR, '('>\
<RPAR, ')'>\
<PLUS, '+'>\
<EQUAL, '='>\
<DOT, '.'>

## How to Test CSVEase Lexer

### Using Docker
In order for easy testing, we have provided a Dockerfile which uses the official Python image from the Docker Hub. 

To build the Docker image, run `docker build -t csvease .`

To run the container, run `docker run -it --rm csvease`

Once you run the container, the container will automatically run the bash script that we developed, `test.sh`. We have included 5 sample programs in the `/sample_programs` directory. The script automates the testing process by providing the user with all the available sample programs, and allowing the user to test which one to run. 

More details on the sample programs and their expected outputs below.

### Using Python 
If the user already has Python installed, to run our testing script. 

Run `chmod +x test.sh`

Then, run `./test.sh`

## Sample Program Output

In order to run the sample programs with CSVease lexer, simply execute the bash script `./test.sh`. All the sample programs are provided in the /sample_program directory. The script starts an interactive session, allowing the user to test any of the provided sample programs. 

`sample_programs/easy.ease` -> Simple keyword and identifier parsing
```
<KEYWORD, 'LOAD'>
<WHITESPACE, ' '>
<KEYWORD, 'DATA'>
<WHITESPACE, ' '>
<KEYWORD, 'INTO'>
<WHITESPACE, ' '>
<IDENTIFIER, 'sales_data'>
```
`sample_programs/error.ease` -> Testing each type of CSVease Lever Error

```
There were 4 errors in sample_programs/error.ease:

Line 2: LOAD "data/file.csv INTO dataset_1'
ERROR Unterminated string literal: "data/file.csv INTO dataset_1'
Line 3: LOAD "("data/file.csv','data/file1.csv')" INTO dataset_1
ERROR Unexpected character: '/'.
Line 6: GET 50 COLUMNS from 123table
ERROR Invalid sequence: `123table`
Line 9: ~ SELECT 
ERROR Unexpected character: '~'.
```

`sample_programs/hard.ease` -> Complex string parsing
```
<KEYWORD, 'LOAD'>
<WHITESPACE, ' '>
<STRING, '('data/file.csv','data/file1.csv')'>
<WHITESPACE, ' '>
<KEYWORD, 'INTO'>
<WHITESPACE, ' '>
<IDENTIFIER, 'dataset_1'>
```

`sample_programs/medium.ease` -> String and Integer Parsing
```
<KEYWORD, 'GET'>
<WHITESPACE, ' '>
<INTEGER, '50'>
<IDENTIFIER, 'COLUMNS1'>
<PLUS, '+'>
<IDENTIFIER, 'COLUMNS_1'>
<WHITESPACE, ' '>
<KEYWORD, 'FROM'>
<WHITESPACE, ' '>
<IDENTIFIER, 'table1'>
```

`sample_programs/whitespace.ease` -> Tests for whitespace
```
<IDENTIFIER, 'sub_table'>
<WHITESPACE, ' '>
<EQ, '='>
<WHITESPACE, ' '>
<KEYWORD, 'GET'>
<WHITESPACE, ' '>
<LPAR, '('>
<IDENTIFIER, 'NAME'>
<COMMA, ','>
<IDENTIFIER, 'AGE'>
<COMMA, ','>
<WHITESPACE, ' '>
<IDENTIFIER, 'YEAR'>
<RPAR, ')'>
<WHITESPACE, ' '>
<KEYWORD, 'IN'>
<WHITESPACE, ' '>
<IDENTIFIER, 'table1'>
<IDENTIFIER, 'sub_table_1'>
<EQ, '='>
<KEYWORD, 'GET'>
<LPAR, '('>
<IDENTIFIER, 'NAME'>
<COMMA, ','>
<IDENTIFIER, 'AGE'>
<COMMA, ','>
<IDENTIFIER, 'YEAR'>
<RPAR, ')'>
<WHITESPACE, ' '>
<KEYWORD, 'IN'>
<WHITESPACE, ' '>
<IDENTIFIER, 'table1'>
```





S -> AssignStmt | GetStmt | LoadStmt | OutputStmt
AssignStmt -> Identifier = RightStmt
RightStmt -> GetStmt | LoadStmt
GetStmt -> GET GetTarget FROM Identifier
GetTarget -> ColumnList | Identifier
ColumnList -> '(' IdList ')'
IdList -> Identifier IdListTail
IdListTail -> ',' Identifier IdListTail | ε
LoadStmt -> LOAD String
OutputStmt -> OUTPUT Identifier TO String AS FileType
FileType -> CSV | JPEG | PDF
