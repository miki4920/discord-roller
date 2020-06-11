from OperationTree.Operators import *
from ErrorHandler import TooManyOperators


def is_number(token):
    if token not in ["+", "-", "*", "/", "(", ")", "%"]:
        return True
    return False


def peek(stack):
    return stack[-1] if stack else None


def greater_precedence(op1, op2):
    precedences = {'>': 0, '<': 0, '+': 1, '-': 1, '*': 2, '/': 2, '//': 2, "%": 2}
    return precedences[op1] > precedences[op2]


def apply_operator(operants, values, tokenized_expression):
    operators = {">": bigger_than,
                 "<": smaller_than,
                 "+": add,
                 "-": sub,
                 "*": mul,
                 "/": true_div,
                 "//": floor_div,
                 "%": mod}
    try:
        operation = operators[operants.pop()]
        right = values.pop()
        left = values.pop()
    except IndexError:
        raise TooManyOperators(tokenized_expression)
    values.append(operation(left, right))


def tokenizer(expression):
    tokens = []
    expression = list(expression)
    number_string = ""
    operator_before = True
    for token in expression:
        if not is_number(token) and not operator_before:
            operator_before = True
            if len(number_string) > 0:
                tokens.append(number_string)
            number_string = ""
            tokens.append(token)
        else:
            operator_before = False
            number_string += token
    if len(number_string) != 0:
        tokens.append(number_string)
    return tokens


def shunting_yard_algorithm(tokenized_expression):
    tokens = tokenized_expression
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values, tokenized_expression)
                top = peek(operators)
            operators.pop()
        else:
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values, tokenized_expression)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values, tokenized_expression)
    return values[0]
