# CSVeaseLexer, CSVeaseParser, and CSVeaseGenerator 

Developers: Phillip Le (pnl2111) and Yue Sun (ys3535)

Demo Video: https://www.youtube.com/watch?v=L6ttwPFsqtk

## Algorithm Overview:

We generate the python code by walking through the abstract syntax tree, we start from the root of the tree, generate code for each subtrees first, then apply the parent operator to combine the subtrees together. For example, the assignment statement will first evaluate the first child which is an identifier, then evaluate the second child which is a more complicated statement, then combine them together with equal (=) sign into the python code. 

## Error Propogation:

### CSVeaseLexer
We developed the CSVeaseLexer to parse the entire input and keep track of errors. At the end of processing the input file, the Lexer will have collected and logged all the line numbers of erros that have come up during this phase. These errors include:
1. InvalidSequence 
2. InvalidString 
3. UnexpectedCharacter
In the case where the lexer has detected any error, there will be no tokens generated.

### CSVeaseParser
Error handling in CSVeaseParse takes a different approach. The parser will halt execution when an error is encountered and raise a ParserError Exception with the indicated cause. Here are the errors that we detected (including but not limited to): 
1. Invalid GET statement 
2. Invalid LOAD statement 
3. Missing Identifier 

### CSVeaseGenerator
Errors coming from this phase we predict are coming from the actual execution of the program itself. Since our coding language generated Python, any errors that you can see coming from the generator are Python compilation errors that we capture and cast as errors coming from compiling csvease code (technically it is!)

Example:
1. User provides an incorrect path to their CSV file
2. Invalid sequence of statements 

### Putting it all together:
Since each phase handles errors differently. In order for us to be able to discern from which step an error is coming from. We implemented the following when you run input code. Here is the referenced code:

```
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
```

## Sample Programs 

We provided the following test programs in the `input/generator` which would work and execute with no errors. Note there are two input directories for the generator. If running locally, please use the input programs in `input/generator`, if using Docker, the `input/generatorDocker` will be copied into the home directory of the container. Instructions below for exactly how to run/test our coding language.

1. basic.ease
- Load input/generator/csv/student_grades.csv
- Print columns 
- Print rows 
- Get NAME, MATH_SCORE from csv 
- Get NAME, SCIENCE_SCORE from csv 
- Output to seperate files

2. chained_operations.ease
- Load input/generator/csv/employee.csv
- Get DEPARTMENT, SALARY, YEARS_EXPERIENCE from csv
- Print columns 
- Print rows 
- Create bar chart with DEPARTMENT and SALARY and writes to jpeg 
- Writes csv

3. original.ease
- Load input/generator/csv/class_roster.csv
- Print columns 
- Print rows 
- Get NAME, AGE, YEAR from csv 
- Output csv 
- Output pdf 
- Output jpeg

4. visualization.ease
- Load input/generator/csv/sales_2023.csv
- Get MONTH, REVENUE from csv 
- Get PRODUCT, UNITS_SOLD from csv 
- Create bar chart with MONTH and REVENUE and writes to jpeg 
- Output csv 

5. weather_analysis.ease
- Load input/generator/csv/weather_data.csv
- Print columns 
- Print rows 
- Get MONTH, AVG_TEMP, MAX_TEMP, MIN_TEMP
- Get MONTH, RAINFALL, HUMIDITY
- Create bar chart with MONTH, AVG_TEMP, MAX_TEMP, MIN_TEMP and writes to jpeg 
- Create bar chart with  MONTH, RAINFALL, HUMIDITY and writes to jpeg 
- Output csv 

We provided the following test programs in the `input/generator` which would output errors.

1. lexer_error.ease -- `CSVeaseLexer: Line 1 -- Unexpected character: '~'.`
2. parser_error.ease --  `CSVeaseParser: Token mismatch: expected FROM, got IDENTIFIER`
3. generator_error.ease -- `CSVeaseGenerator: Could not find 'input/generator/csv/does_not_exist.csv'`

We also provided data from which the input programs will often reference in their execution in `input/generator/csv`

1. class_roster.csv        
2. science_results.csv
3. employee.csv            
4. student_grades.csv
5. sales_2023.csv          
6. weather_data.csv

## How to run?

Now that we have the code generator, `CSVeaseGenerator`, we can see the full pipeline and run input programs like any other coding language. 

### Using Docker

For the best experience we reccomend using Docker to test CSVease. You can build and run the image with the following commands:

1. `docker build -t csvease .`
2. `docker run -it csvease`

During the build process, the input/generatorDocker directory will be copied into the Docker container's home directory. From which you can simply run:
`csvease <input_file_name>.ease`

Note VIM is installed in the Docker image, so you can make edits to the input files directly in the image. To view the contents of an output file, run `cat name_of_file`. However, you will not be able to view JPEGS or PDF files in any meaningful way if testing with Docker. 

### Running locally

We have provided a shell script which you can run by doing the following

1. `chmod +x csvease`
2. `./csvease input/generator/<input_file>`

**Note that when running locally, your machine must have pandas and matplotlib Python libraries already installed.**

### Testing previous parts

In the case where you would like to test previous parts, this can be done locally. Simply run the commands: 

1. `chmod +x test.sh`
2. `./test.sh`

This will run a script which would allow you to test both the parser and lexer. This is optional as the generator already includes these processes in the pipeline.

That concludes our CSVeaseGenerator. Thank you for a great semester.

### 

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

# CSVeaseParser

### Link to video: https://youtu.be/_Jc5E0kkL3Q

## Context Free Grammar
```
S -> StmtList

StmtList -> BaseStmt StmtListTail

StmtListTail -> BaseStmt StmtListTail | ε

BaseStmt -> AssignStmt | ConvertStmt | GetStmt | LoadStmt | ShowStmt | OutputStmt

AssignStmt -> IDENTIFIER EQ BaseStmt

ConvertStmt -> CONVERT IDENTIFIER TO ChartType

GetStmt -> GET GetTarget FROM IDENTIFIER

GetTarget -> LPAREN ColumnList RPAREN | IDENTIFIER

ColumnList -> IDENTIFIER ColumnListTail

ColumnListTail -> COMMA IDENTIFIER ColumnListTail | ε

LoadStmt -> LOAD STRING

OutputStmt -> OUTPUT IDENTIFIER TO STRING AS FileType

ShowStmt -> SHOW ShowOptions IDENTIFIER

ShowOptions -> ROWS | COLUMNS

FileType -> CSV | JPEG | PDF

ChartType -> BARCHART
```
## Terminals
```python
self.terminals = [
            'IDENTIFIER', 'SHOW', 'GET', 'LOAD', 'INTO', 'FROM', 'TO', 'OUTPUT',
            'ROWS', 'COLUMNS', 'LPAREN', 'COMMA', 'RPAREN', 'LPAR', 'RPAR',
            'OUTPUT', 'CSV', 'JPEG', 'PDF', 'EQ', 'PLUS', 'AS', 'STRING',
            'IN', 'AVG', 'GROUP_BY', 'CONVERT', 'BARCHART'
        ]
```
## NonTerminals
1. S 
2. StmtList 
3. StmyListTail 
4. BaseStmt 
5. AssignStmt
6. ConvertStmt 

## How to Test CSVEase Parser

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