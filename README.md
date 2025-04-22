Usage:
  Run the file "__main__.py" to start the program. The console will prompt the user for an input or command, and will continue until the session is terminated.

Commands: 
  "exit" or "quit" will terminate the program.
  "clear" will clear the console.
  "M = E" will save a expression to a macro, where M is the name and E is the expression

Conventions:
  Macro: The user can bind expressions to a name for improved readibility. Macros must begin with an uppercase letter and can be defined in the console, or using the "macros.txt" file.
  Variable: Variables must be a single lowercase letter.
  Abstraction: Abstractions must begin with either "λ" or "\", followed by any number of variables, and terminating with ".T", where T is a term.
    Ex. 1: "λx. T"
    Ex. 2: "\xyz. \a. T"
  Application: Applications must be surrounded by parentheses. The parser is currently very strict about this and won't accept shortened inputs such as "abcd" instead of (((ab)c)d).
    Ex. 1: "(x T)"
    Ex. 2: "(T x)"
    Ex. 3: "(T T)"
    Ex. 4: "(x y)"
  The parser will ignore whitespace in expressions. "((\x.x)(yz))" is the same as "((\x. x) (y z))".

Macros: The following macros are already implemented in the "macros.txt" file.
  False = \xy.y
  True = \xy.x
  Not = \x.((x(False))(True))
  And = \xy.((xy)(False))
  
  Zero = \fx.x
  One = \fx.(fx)
  Two = \fx.(f(fx))
  Three = \fx.(f(f(fx)))
  Four = \fx.(f(f(f(fx))))
  Five = \fx.(f(f(f(f(fx)))))
  Six = \fx.(f(f(f(f(f(fx))))))
  Seven = \fx.(f(f(f(f(f(f(fx)))))))
  Eight = \fx.(f(f(f(f(f(f(f(fx))))))))
  Nine = \fx.(f(f(f(f(f(f(f(f(fx)))))))))
  Ten = \fx.(f(f(f(f(f(f(f(f(f(fx))))))))))
  
  Succ = \a.\fx.(f((af)x))
  Add = \ab.((a(Succ))b)
  Mult = \ab.\f.(a(bf))

Examples: The following are some examples of inputs with their outputs that I know work.
  \x.x -> λx.x
  ((\x.x)(yz)) -> (yz)
  ((\x.(xx))y) -> (yy)
  ((\x.(xy))(\z.z)) -> y
  ((\x.((xx)y))(\z.z)) -> y
  ((\x.((\y.(yx))z))v) -> (zv)
  ((\xyz.(xy))(\x.x)) -> λy.λz.y
  ((\xy.x)y) -> λa.y
  ((\x.((x x)y))(\x.((x x)y))) -> Recursion Error
  ((\x.(xx))(\x.(xx))) -> ((λx.(xx))(λx.(xx)))
  
  ((Not)(False)) -> λx.λy.x
  ((Not)(True)) -> λx.λy.y
  
  (((And)(False))(False)) -> λx.λy.y
  (((And)(False))(True)) -> λx.λy.y
  (((And)(True))(False)) -> λx.λy.y
  (((And)(True))(True)) -> λx.λy.x
  
  ((Succ)(Zero)) -> λf.λx.(fx)
  (((Add)(Zero))(One)) -> λf.λx.(fx)
  (((Add)(One))(Zero)) -> λf.λx.(fx)
  (((Add)(One))(One)) -> λf.λx.(f(fx))
