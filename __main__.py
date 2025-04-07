import sys
from parser import Parser, LambdaSyntaxError, InvalidCharacterError, UnbalancedParenthesesError

def main():
    parser = Parser()
    while True:
        inp = str(input("Enter an expression: ")).replace(" ", "")
        if (inp == "exit"):
            return 0
        elif ("=" in inp):
            index = inp.index("=")
            name = inp[:1].capitalize + inp[1:index]

            try:
                parser.create_macro(name, inp[index+1:])
            except:
                print("TODO: error")
                continue
        else:
            try:
                expr = parser.preprocess(inp)
                print(": " + str(expr))
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