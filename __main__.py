import sys
import os
from parser import Parser, LambdaSyntaxError, InvalidCharacterError, UnbalancedParenthesesError
from term import Term, Variable, Term

def main():
    parser = Parser()
    while True:
        inp = str(input("Enter an expression: ")).replace(" ", "")
        if (inp == "exit"):
            return 0
        elif (inp == "clear"):
            clear = lambda: os.system('cls')
            clear()
        elif ("=" in inp):
            index = inp.index("=")
            name = inp[0].capitalize() + inp[1:index]

            try:
                parser.create_macro(name, inp[index + 1:])
            except:
                print("Error creating macro")
        else:
            try:
                expr = parser.preprocess(inp)
                print(f"Expression: {expr}")
                while True:
                    reduced_expr = Term.beta_reduce(expr)
                    if (reduced_expr == expr):
                        break
                    else:
                        print(f"Reduced to: {reduced_expr}")
                        expr = reduced_expr

                print(f"Final expression:  {expr}")
            except LambdaSyntaxError as error:
                print(error.message)
                continue
            except InvalidCharacterError as error:
                print(error.message)
                continue
            except UnbalancedParenthesesError as error:
                print(error.message)
                continue

if __name__ == '__main__':
    sys.exit(main()) 