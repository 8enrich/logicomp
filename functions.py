"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import * 


def length(formula: Formula):
    """Determines the length of a formula in propositional logic."""
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return length(formula.inner) + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1
    return 0


def subformulas(formula: Formula):
    """Returns the set of all subformulas of a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for subformula in subformulas(my_formula):
        print(subformula)

    This piece of code prints p, s, (p v s), (p → (p v s))
    (Note that there is no repetition of p)
    """

    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return {formula}.union(subformulas(formula.inner))
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        sub1 = subformulas(formula.left)
        sub2 = subformulas(formula.right)
        return {formula}.union(sub1).union(sub2)
    return {}

#  we have shown in class that, for all formula A, len(subformulas(A)) <= length(A).


def atoms(formula: Formula):
    """Returns the set of all atoms occurring in a formula.

    For example, observe the piece of code below.

    my_formula = Implies(Atom('p'), Or(Atom('p'), Atom('s')))
    for atom in atoms(my_formula):
        print(atom)

    This piece of code above prints: p, s
    (Note that there is no repetition of p)
    """
    if isinstance(formula, Atom):
        return {formula}
    if isinstance(formula, Not):
        return atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        atoms1 = atoms(formula.left)
        atoms2 = atoms(formula.right)
        return (atoms1).union(atoms2)
    return {}


def number_of_atoms(formula: Formula):
    """Returns the number of atoms occurring in a formula.
    For instance,
    number_of_atoms(Implies(Atom('q'), And(Atom('p'), Atom('q'))))

    must return 3 (Observe that this function counts the repetitions of atoms)
    """
    if isinstance(formula, Atom):
        return 1
    if isinstance(formula, Not):
        return number_of_atoms(formula.inner)
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        num_of_atoms1 = number_of_atoms(formula.left)
        num_of_atoms2 = number_of_atoms(formula.right)
        return num_of_atoms1 + num_of_atoms2


def number_of_connectives(formula: Formula):
    """Returns the number of connectives occurring in a formula."""
    if isinstance(formula, Atom):
        return 0
    if isinstance(formula, Not):
        num_of_conn = number_of_connectives(formula.inner)
        return num_of_conn + 1
    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        num_of_conn1 = number_of_connectives(formula.left)
        num_of_conn2 = number_of_connectives(formula.right)
        return 1 + num_of_conn1 + num_of_conn2

def is_literal(formula: Formula):
    """Returns True if formula is a literal. It returns False, otherwise"""
    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_literal(formula.inner)
    if isinstance(formula, (Implies, And, Or)):
        return False

def substitution(formula: Formula, old_subformula: Formula, new_subformula: Formula):
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""
    if isinstance(formula, Not):
        formula.inner = substitution(formula.inner, old_subformula, new_subformula)
    if isinstance(formula, (Or, Implies, And)):
        formula.right = substitution(formula.right, old_subformula, new_subformula)
        formula.left = substitution(formula.left, old_subformula, new_subformula)
    if formula == old_subformula:
        formula = new_subformula
    return formula

def is_clause(formula: Formula):
    """Returns True if formula is a clause. It returns False, otherwise"""
    if isinstance(formula, (Atom, Not)):
        return is_literal(formula)
    if isinstance(formula, Or):
        return is_clause(formula.left) and is_clause(formula.right)
    if isinstance(formula, (Implies, And)):
        return False

def is_negation_normal_form(formula: Formula):
    """Returns True if formula is in negation normal form.
    Returns False, otherwise."""
    if isinstance(formula, Atom):
        return True
    if isinstance(formula, Not):
        return is_negation_normal_form(formula.inner)
    if isinstance(formula, Implies):
        return False
    if isinstance(formula, (And, Or)):
        return is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right)

def is_cnf(formula: Formula):
    """Returns True if formula is in conjunctive normal form.
    Returns False, otherwise."""
    if isinstance(formula, (Atom, Not, Implies, Or)):
        return is_clause(formula)
    if isinstance(formula, And):
        return is_cnf(formula.left) and is_cnf(formula.right)

def is_term(formula: Formula):
    """Returns True if formula is a term. It returns False, otherwise"""
    if isinstance(formula, (Atom, Not, Implies, Or)):
        return is_literal(formula)
    if isinstance(formula, And):
        return is_term(formula.left) and is_term(formula.right)

def is_dnf(formula: Formula):
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""
    if isinstance(formula, (Atom, Not, Implies, And)):
        return is_term(formula)
    if isinstance(formula, Or):
        return is_dnf(formula.left) and is_dnf(formula.right)

def is_decomposable_negation_normal_form(formula: Formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========
