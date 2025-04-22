import copy
from macro import Macro
from term import Abstraction, Application, Variable, Term

class Parser:
    def __init__(self):
        self.macros = []

    # Saves a macro
    def create_macro(self, name, expr):
        if name.isalpha():
            expr = self.preprocess(expr)
            expr = Parser.parse(expr)
            while True:
                reduced_expr = Term.beta_reduce(copy.deepcopy(expr))
                if (str(reduced_expr) == str(expr)):
                    break
                else:
                    expr = reduced_expr
            for m in self.macros:
                if m.name == name:
                    m.expr = expr
                    return
            
        self.macros.append(Macro(name, expr))

    def preprocess(self, input):
        for m in self.macros:   # Searches for macros in the input expression
            input = input.replace(m.name, str(m.expr))
        parentheses_count = 0
        for char in input:
            if char == "(":
                parentheses_count += 1
            elif char == ")":
                parentheses_count -= 1
            if parentheses_count < 0:
                raise UnbalancedParenthesesError()

        if not parentheses_count == 0:
            raise UnbalancedParenthesesError()

        return input

    # The main parser function
    def parse(input):
        match input[0]:
            case "λ" | "\\":
                return Parser.parse_abstraction(input[1:])
            case "(":
                return Parser.parse_application(input[1:len(input) - 1])
            case var if Parser.is_variable(var):
                return Variable(var)
            case other:
                raise InvalidCharacterError(str(other), input)

    def parse_abstraction(input):
        next_char = input[0]
        if Parser.is_variable(next_char):
            return Abstraction(Variable(next_char), Parser.parse_abstraction(input[1:]))
        elif next_char == ".":
            return Parser.parse(input[1:])
        else:
            raise LambdaSyntaxError(".", next_char, input)

    def parse_application(input):
        parentheses_count = 0   # Counts open parentheses to determine if the current value of the loop is enclosed
        first_term_index = -1
        for i in range(0, len(input)):
            match input[i]:
                case "(":
                    parentheses_count += 1
                case ")":
                    parentheses_count -= 1
                    if first_term_index == -1 and parentheses_count == 0:
                        first_term_index = i
                    elif parentheses_count == 0:
                        left = input[:first_term_index + 1]
                        right = input[first_term_index + 1:]

                        if left[1] == "λ" or left[1] == "\\":
                            left = left[1:len(left) - 1]
                        if right[1] == "λ" or right[1] == "\\":
                            right = right[1:len(right) - 1]

                        return Application(Parser.parse(left), Parser.parse(right))       # Case that term is an application of complex terms
                case var if Parser.is_variable(var):
                    if parentheses_count == 0 and i == 0:
                        if len(input) == 2:
                            return Application(Variable(input[0]), Variable(input[1]))
                        else:
                            right = input[1:]
                            if right[1] == "λ" or right[1] == "\\":
                                right = right[1:len(input)]
                            return Application(Variable(var), Parser.parse(right))
                    elif parentheses_count == 0 and (not first_term_index == -1):
                        left = input[0:first_term_index + 1]
                        if left[1] == "λ" or left[1] == "\\":
                            left = left[1:first_term_index]
                        return Application(Parser.parse(left), Variable(var))

    def is_variable(name):
        return len(name) == 1 and name in "abcdefghijklmnopqrstuvwxyz" and name.islower()
    
class LambdaSyntaxError(Exception):
    def __init__(self, expected, actual, expression):
        self.message = f"Error processing abstraction: expected {expected}, actual {actual} in {expression}"
        super().__init__(self.message)

class InvalidCharacterError(Exception):
    def __init__(self, char, expression):
        self.message = f"Invalid character: {char} in {expression}"
        super().__init__(self.message)

class UnbalancedParenthesesError(Exception):
    def __init__(self):
        self.message = "Unbalanced parentheses"
        super().__init__(self.message)