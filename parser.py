from macro import Macro
from term import Abstraction, Application, Variable, Term

class Parser:
    def __init__(self):
        self.macros = []

    def create_macro(self, name, expr):
        if name.isalpha():
            term = self.preprocess(expr)
            term = Term.beta_reduce(term)
            for m in self.macros:
                if m.name == name:
                    m.expr = term
                    return
            
        self.macros.append(Macro(name, term))

    def preprocess(self, input):
        for m in self.macros:   # Searches for macros in the input expression
            input = input.replace(m.name, m.expression)
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

        return Parser.parse(input)

    def parse(input):
        match input[0]:
            case "λ" | "\\":
                print("Found Lambda")
                return Parser.parse_abstraction(input[1:])
            case "(":
                print("Found (")
                return Parser.parse_application(input[1:len(input) - 1])
            case var if Parser.is_variable(var):
                print("Found Var")
                return Variable(var)
            case other:
                raise InvalidCharacterError(str(other), input)

    def parse_abstraction(input):
        print(f"Abs Recieved: {input}")
        next_char = input[0]
        if Parser.is_variable(next_char):
            return Abstraction(Variable(next_char), Parser.parse_abstraction(input[1:]))
        elif next_char == ".":
            return Parser.parse(input[1:])
        else:
            raise LambdaSyntaxError(".", next_char, input)

    def parse_application(input):
        print(f"App Recieved: {input}")
        parentheses_count = 0   # Counts open parentheses to determine if the current value of the loop is enclosed
        first_term_index = -1
        found_lambda = False
        for i in range(0, len(input)):
            match input[i]:
                case "(":
                    print("Application: found (")
                    parentheses_count += 1
                case ")":
                    parentheses_count -= 1
                    if first_term_index == -1 and parentheses_count == 0:
                        if found_lambda:
                            return Application(Parser.parse(input[:i]), Parser.parse(input[i:]))
                        first_term_index = i
                    elif parentheses_count == 0:
                        return Application(Parser.parse(input[1:first_term_index]), Parser.parse(input[first_term_index:len(input) - 1]))       # Case that term is an application of complex terms
                case var if Parser.is_variable(var):
                    print(f"Application: found var {var}")
                    if parentheses_count == 0 and i == 0:
                        return Application(Variable(var), Parser.parse(input[1:]))
                    elif parentheses_count == 0:
                        return Application(Parser.parse(input[:len(input) - 1]), Variable(var))
                case "λ" | "\\":
                    found_lambda = True
                    if (not first_term_index == -1) and parentheses_count == 0:
                        return Application(Parser.parse(input[1:first_term_index]), Parser.parse(input[first_term_index:]))

    def is_variable(name):
        return len(name) == 1 and name.isalpha() and name.islower()
    
class LambdaSyntaxError(Exception):
    def __init__(self, expected, actual, expression):
        message = "Error processing abstraction: expected {expected}, actual {actual} in {expression}"
        super().__init__(message)

class InvalidCharacterError(Exception):
    def __init__(self, char, expression):
        message = "Invalid character: {char} in {expression}"
        super().__init__(message)

class UnbalancedParenthesesError(Exception):
    def __init__(self):
        message = "Unbalanced parentheses"
        super().__init__(message)