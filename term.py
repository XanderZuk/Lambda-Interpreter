class Term:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Abstraction(Term):
    def __init__(self, variable, term):
        super().__init__(variable, term)

    def __str__(self):
        return f"λ{self.left}.{str(self.right)}"

class Application(Term):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        return f"({self.left}{self.right})"

class Variable(Term):
    def __init__(self, name):
        super().__init__(None, None)
        self.name = name

    def __str__(self):
        return self.name