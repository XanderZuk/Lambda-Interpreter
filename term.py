class Term:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def alpha_reduce(term):
        bound_vars = Term.bound_variables(term.left)    # List of bound variables in the left side of the application
        free_vars = Term.free_variables(term.right)     # List of free variables in the right side of the application
        # Renames any conflicting variables
        for s in bound_vars:    
            if s in free_vars:
                #print(f"Substituting {s} for {new_var}")
                new_var = Term.next_variable_name(term)
                term.left = Term.substitute(term.left, s, Variable(new_var))
        return term

    def beta_reduce(redex):
        if isinstance(redex.left, Abstraction) and isinstance(redex, Application):
            redex = Term.alpha_reduce(redex)
            return Term.substitute(redex.left.right, redex.left.left.name, redex.right) 
        else:
            return redex
        
    def substitute(term, var_name, new_term):
        #print(f"Substitution input: {term}")
        if isinstance(term, Abstraction):
            if var_name == term.left.name:
                term.left = new_term
            term.right = Term.substitute(term.right, var_name, new_term)
        elif isinstance(term, Application):
            term.left = Term.substitute(term.left, var_name, new_term)
            term.right = Term.substitute(term.right, var_name, new_term)
        elif isinstance(term, Variable):
            if term.name == var_name:
                term = new_term
        return term
    
    def bound_variables(term):
        bound_variables_list = []
        def find_bound_variables(term):
            if isinstance(term, Abstraction):
                bound_variables_list.append(term.left.name)
                find_bound_variables(term.right)
            elif isinstance(term, Application):
                find_bound_variables(term.left)
                find_bound_variables(term.right)
        find_bound_variables(term)
        return bound_variables_list

    def free_variables(term):
        free_variables_list = []
        bound_variables_list = []
        def find_free_variables(term):
            if isinstance(term, Abstraction):
                if not term.left.name in bound_variables_list:
                    bound_variables_list.append(term.left.name)
                    find_free_variables(term.right)
                    bound_variables_list.remove(term.left.name)
            elif isinstance(term, Application):
                find_free_variables(term.left)
                find_free_variables(term.right)
            elif isinstance(term, Variable):
                if (not term.name in bound_variables_list) and (not term.name in free_variables_list):
                    free_variables_list.append(term.name)
                    return
        find_free_variables(term)
        return free_variables_list
            
    def next_variable_name(redex):
        def current_variable_names(term, list):
            if isinstance(term, Abstraction):
                if (not term.left.name in list):
                    list.append(term.left.name)
            elif isinstance(term, Application):
                current_variable_names(term.left, list)
                current_variable_names(term.right, list)
            elif isinstance(term, Variable):
                if (not term.name in list):
                    list.append(term.name)

        names_list = []
        current_variable_names(redex, names_list)
        for s in "abcdefghijklmnopqrstuvwxyz":
            if not s in names_list:
                return s
        
class Abstraction(Term):
    def __init__(self, variable, term):
        super().__init__(variable, term)

    def __str__(self):
        return f"λ{self.left}.{str(self.right)}"

class Application(Term):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __str__(self):
        left = self.left
        right = self.right
        if isinstance(self.left, Abstraction):
            left = f"({self.left})"
        if isinstance(self.right, Abstraction):
            right = f"({self.right})"
        return f"({left}{right})"

class Variable(Term):
    def __init__(self, name):
        super().__init__(None, None)
        self.name = name

    def __str__(self):
        return self.name