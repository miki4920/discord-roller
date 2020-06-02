import operator


def parse_equation_into_list(equation):
    joined_numbers = []
    number_string = ""
    for token in list(equation):
        if token in ["+", "-", "*", "/", "(", ")"]:
            if len(number_string) > 0:
                joined_numbers.append(number_string)
            number_string = ""
            joined_numbers.append(token)
        else:
            number_string += token
    return joined_numbers


def parse_tree(equation):
    tree = Tree()
    for token in equation:
        if token == "(":
            tree.add_left()
        elif token in ["+", "-", "*", "/"]:
            tree.current_node.value = token
            tree.add_right()
        elif token not in ["+", "-", "*", "/", "(", ")"]:
            tree.current_node.value = token
            tree.current_node = tree.current_node.parent
        elif token == ")":
            tree.current_node = tree.current_node.parent
    return tree


def evaluate(node):
    opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    left = node.left
    right = node.right
    if left and right:
        fn = opers[node.value]
        return fn(evaluate(left), evaluate(right))
    else:
        return node.value


class Node(object):
    def __init__(self, value=None, parent=None, left=None, right=None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


class Tree(object):
    def __init__(self, root=None):
        self.root = Node(root)
        self.current_node = self.root

    def add_left(self, value=None):
        self.current_node.left = Node(value, parent=self.current_node)
        self.current_node = self.current_node.left

    def add_right(self, value=None):
        self.current_node.right = Node(value, parent=self.current_node)
        self.current_node = self.current_node.right
