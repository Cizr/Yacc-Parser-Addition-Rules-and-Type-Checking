import ply.lex as lex
import ply.yacc as yacc

# Token def
tokens = ("PLUS", "INT", "REAL", "ID")

# Regular expression for the PLUS token
t_PLUS = r"\+"

# Define a rule for the REAL token
def t_REAL(t):
    r"[0-9]+\.[0-9]+"
    t.value = float(t.value)
    return t

# Define a rule for the INT token
def t_INT(t):
    r"[0-9]+"
    t.value = int(t.value)
    return t

# Define a rule for the ID token
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Ignore whitespaces and tabs
t_ignore = " \t"

# Handle lexical errors
def t_error(t):
    print("Lexical error")
    t.lexer.skip(1)

# Custom class for more readable token printing
class LexTokenWithShortStr(lex.LexToken):
    def __str__(self):
        return f"LexToken({self.type}, {self.value})"


lexer = lex.lex()
lexer.LexToken = LexTokenWithShortStr  # better token printing

# rules
def p_expression_binary(p):
    '''
    expression : expression PLUS expression
               | value
    '''
    if len(p) == 2:
        # If there's only one value set the result to that value
        p[0] = {'type': p[1]['type'], 'value': p[1]['value']}
    else:
        # If there's an operation calculate the result
        p[0] = {'type': checkType(p[1]['type'], p[3]['type']), 'value': calculate(p[1], p[2], p[3])}

def p_value_number(p):
    '''
    value : INT
          | REAL
    '''
    # Set the result as a float if it's a real number otherwise as an integer
    p[0] = {'type': 'float' if '.' in str(p[1]) else 'int', 'value': p[1]}

def p_error(p):
    print(f"Syntax error: {p}")

# check type compatibility
def checkType(type1, type2):
    if type1 == 'float' or type2 == 'float':
        return 'float'
    else:
        return 'int'

# calculate the result of the expression
def calculate(operand1, operator, operand2):
    if operator == '+':
        return operand1['value'] + operand2['value']
    else:
        print(f"Error: Unsupported operator - {operator}")
        return None


lexer = lex.lex()
parser = yacc.yacc()

# Example 
input_code = '3 + 3'
lexer.input(input_code)

# Print tokens generated by the lexer
for tok in lexer:
    print(tok)

result = parser.parse(input_code)
if result:
    print("Expression result:", result['value'])
else:
    print("Syntax error in the expression")
