from DiceOperations.Operators import *
from ErrorHandler import too_many_operators, wrong_command_format
import re


def is_number(token):
    if token not in ["+", "-", "*", "/", "//", "(", ")", "%", ">", "<", "<=", ">="]:
        return True
    return False


def peek(stack):
    return stack[-1] if stack else None


def greater_precedence(op1, op2):
    precedences = {'>': 0, '<': 0, '>=': 0, '<=': 0, '+': 1, '-': 1, '*': 2, '/': 2, '//': 2, "%": 2}
    return precedences[op1] > precedences[op2]


def apply_operator(operants, values):
    operators = {">": bigger_than,
                 "<": smaller_than,
                 ">=": bigger_equal_than,
                 "<=": smaller_equal_than,
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
    except (IndexError, KeyError) as e:
        raise too_many_operators()
    try:
        values.append(operation(left, right))
    except ValueError:
        raise wrong_command_format()


def tokenizer(expression):
    tokens = []
    expression = expression.replace(" ", "")
    expression = re.findall("[^<=|>=|<|>|%|//|/|\*|\-|\+|\(|\)]+|<=|>=|<|>|%|//|/|\*|-|\+|\(|\)", expression)
    operator_before = True
    operator_string = ""
    for token in expression:
        if is_number(token) and token:
            operator_string += token
            tokens.append(operator_string)
            operator_string = ""
            operator_before = False
        elif operator_before and token == "-":
            operator_string += token
        elif operator_before and token not in ("(", ")", "-"):
            raise too_many_operators()
        elif not is_number(token) and token not in ("(", ")"):
            tokens.append(token)
            operator_before = True
        else:
            tokens.append(token)
    return tokens


def shunting_yard_algorithm(tokenized_expression):
    tokens = tokenized_expression
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            try:
                operators.pop()
            except IndexError:
                raise too_many_operators()

        else:
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)
    try:
        return int(values[0]) if values[0].is_integer() else float(values[0])
    except AttributeError:
        raise wrong_command_format()
