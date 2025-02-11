from fol_formula import Atom, Not, Implies, And, Or, ForAll, Exists
from term import Con, Var, Fun


def length_fol(formula):
    """Determines the length of a formula in first-order logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, (Not, ForAll, Exists)):
        return length_fol(formula.inner) + 1
    if isinstance(formula, (Implies, And, Or)):
        return length_fol(formula.left) + length_fol(formula.right) + 1
    return 0


def subformulas_fol(formula):
    """Returns the set of all subformulas of a first-order formula"""
    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, (Not, ForAll, Exists)):
        return {formula}.union(subformulas_fol(formula.inner))
    if isinstance(formula, (Implies, And, Or)):
        return {formula}.union(subformulas_fol(formula.left)).union(subformulas_fol(formula.right))
    return set()


def constants_from_term(term):
    """Returns the set of all constant occurring in a term"""
    if isinstance(term, Con):
        return {term}
    if isinstance(term, Var):
        return set()
    if isinstance(term, Fun):
        return set(map(constants_from_term, term.args))
    return set()


def variables_from_term(term):
    """Returns the set of all variables occurring in a term"""
    if isinstance(term, Con):
        return set()
    if isinstance(term, Var):
        return {term}
    if isinstance(term, Fun):
        return set(map(variables_from_term, term.args))
    return set()


def function_symbols_from_term(term):
    """Returns the set of all function symbols occurring in a term
    For example, function_symbols_from_term(Fun('f', [Var('x'), Con('a')]))
    must return {'f'}

    and

    function_symbols_from_term(Fun('g', [Fun('f', [Var('x'), Con('a')])]))
    must return {'f', 'g'}
    """
    if isinstance(term, (Con, Var)):
        return set()
    if isinstance(term, Fun):
        return set(map(function_symbols_from_term, term.args)).union(term.name)
    return set()


def all_constants(formula):
    """Returns the set of all constant occurring in a formula"""
    if isinstance(formula, Atom):
        return set(map(constants_from_term, formula.args))
    if isinstance(formula, (Not, ForAll, Exists)):
        return all_constants(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return all_constants(formula.left).union(all_constants(formula.right))
    return set()


def predicate_symbols(formula):
    """Returns the set of all predicate symbols occurring in a formula.
    For example, predicate_symbols(Or(Atom('P', [Con('a')]), Atom('R', [Var('x')])))
    must return {'P', 'R'}
    """
    if isinstance(formula, Atom):
        return {formula.name}
    if isinstance(formula, (Not, ForAll, Exists)):
        return predicate_symbols(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return predicate_symbols(formula.left).union(predicate_symbols(formula.right)) 
    return set()


def function_symbols(formula):
    """Returns the set of all function symbols occurring in a formula.
    For example, predicate_symbols(Or(Atom('P', [Fun('f', [Con('b'), Var('y')])]),
                                      Atom('P', [Fun('g', [Var('y')])])
                                      )
                                   )
    must return {'f', 'g'}
    """
    if isinstance(formula, Atom):
        return set(map(function_symbols_from_term, formula.args))
    if isinstance(formula, (Not, ForAll, Exists)):
        return function_symbols(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return function_symbols(formula.left).union(function_symbols(formula.right)) 
    return set()


def atoms_fol(formula):
    """Returns the set of all atomic suformulas of a first-order formula"""
    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, (Not, ForAll, Exists)):
        return atoms_fol(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return atoms_fol(formula.left).union(atoms_fol(formula.right))
    return set()


def free_variables(formula):
    """Returns the set of all free variables of a formula"""
    pass
    

def bounded_variables(formula):
    """Returns the set of all bounded variables of a formula"""
    pass


def universal_closure(formula):
    """Returns the universal closure of a formula"""
    pass


def existential_closure(formula):
    """Returns the existential closure of a formula"""
    pass


def number_free_occurrences(var, formula):
    """Returns the number of free occurrences of variable var in formula.
    For example, number_free_occurrences(Var('x'),
                                         ForAll(Var('y'), Implies(And(Atom('P', [Var('x')]),
                                                                      Atom('Q', [Var('y')])),
                                                                  ForAll(Var('x'), Atom('Q', [Var('x')]))
                                                                 )
                                               )
                                        )
    must return 1
    """
    pass


# scope?
# quantifier-free
# closed term / ground terms
# closed formula / sentence
