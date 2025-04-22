import sys
import os
import copy
from parser import Parser, LambdaSyntaxError, InvalidCharacterError, UnbalancedParenthesesError
from term import Term

def main():
    parser = Parser()
    show_steps = False
    recursion_limit = 100

    if len(sys.argv) == 2:
        if sys.argv[1] == "show":
            show_steps = True
        else:
            recursion_limit = int(sys.argv[1])
    elif len(sys.argv) == 3:
        show_steps = True
        recursion_limit = int(sys.argv[2])

    sys.setrecursionlimit(recursion_limit)

    def load_macros():
        print("Loading macros from file...")
        file = open("macros.txt", "r")
        for line in file:
            try:
                stripped = line.strip().replace(" ", "")
                index = stripped.index("=")
                name = stripped[0].capitalize() + stripped[1:index]
                parser.create_macro(name, stripped[index + 1:])
            except:
                print(f"Error loading macro {stripped}")
                continue
        file.close()
            
    load_macros()

    while True:
        inp = str(input("Enter an expression: ")).replace(" ", "")
        if (inp == "quit") or (inp == "exit"):
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
                expr = Parser.parse(expr)
                print(f"Expression: {expr}")
                while True:
                    reduced_expr = Term.beta_reduce(copy.deepcopy(expr))
                    if (str(reduced_expr) == str(expr)):
                        break
                    else:
                        if show_steps:
                            print(f"Reduced to: {reduced_expr}")
                        expr = reduced_expr

                print(f"Final expression: {expr}")
                print("\n")
            except LambdaSyntaxError as error:
                print(error.message)
                continue
            except InvalidCharacterError as error:
                print(error.message)
                continue
            except UnbalancedParenthesesError as error:
                print(error.message)
                continue
            except RecursionError:
                print(f"Max recursion depth exceeded. Term {expr} was too large or resulted in an infinite expansion.")
    
            

if __name__ == '__main__':
    sys.exit(main()) 