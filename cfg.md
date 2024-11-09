S -> A | B | C | D | E | F | Id = S\
A -> LOAD X INTO Id | LOAD X\
X -> DATA | String\
B -> SHOW Y IN Id\
Y -> ROWS | COLUMNS\
C -> GET Z FROM Id\
Z -> int U | U | int ROWS | (T)\
U -> Id Op U | Id\
Op -> + | - | * | /\
T -> Id,T | Id\
D -> AVG (Id) GROUP_BY (Id) IN Id\
E -> OUTPUT Id TO Id AS V\
V -> PDF | CSV | JPG\
F -> CONVERT Id TO W CHART\
W -> BAR | HIST\


