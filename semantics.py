"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms, is_cnf, subformulas, is_literal
from itertools import product
from functools import reduce


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    if isinstance(formula, Atom):
        return interpretation.get(formula.name, None) or interpretation.get(formula, None)
    if isinstance(formula, Not):
        return not truth_value(formula.inner, interpretation)
    if isinstance(formula, Implies):
        return not truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)
    if isinstance(formula, And):
        return truth_value(formula.left, interpretation) and truth_value(formula.right, interpretation)
    if isinstance(formula, Or):
        return truth_value(formula.left, interpretation) or truth_value(formula.right, interpretation)

def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    for row in truth_table(formula):
        if not row[formula]:
            return False
    return True

def satisfiability_brute_force(formula):
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
    for row in truth_table(formula):
        if row[formula]:
            return row
    return False

def all_models(formula):
    models = []
    for row in truth_table(formula):
        if row[formula]:
            models.append(row)
    return models

def truth_table(formula):
    list_atoms = atoms(formula)
    valuations = list(product([True, False], repeat=len(list_atoms)))
    for v in valuations:
        row = {atom: value for atom, value in zip(list_atoms, v)}
        row[formula] = truth_value(formula, row)
        yield row

def remove_implies(formula):
    if isinstance(formula, Not):
        return Not(remove_implies(formula.inner))
    if isinstance(formula, And):
        return And(remove_implies(formula.left), remove_implies(formula.right))
    if isinstance(formula, Or):
        return Or(remove_implies(formula.left), remove_implies(formula.right))
    if isinstance(formula, Implies):
        return Or(Not(remove_implies(formula.left)), remove_implies(formula.right))
    return formula

def de_morgan(formula):
    if isinstance(formula, Not):
        if isinstance(formula.inner, Or):
            return And(Not(de_morgan(formula.inner.left)), Not(de_morgan(formula.inner.right)))
        if isinstance(formula.inner, And):
            return Or(Not(de_morgan(formula.inner.left)), Not(de_morgan(formula.inner.right)))
        return Not(de_morgan(formula.inner))
    if isinstance(formula, And):
        return And(de_morgan(formula.left), de_morgan(formula.right))
    if isinstance(formula, Or):
        return Or(de_morgan(formula.left), de_morgan(formula.right))
    return formula

def remove_double_negation(formula):
    if isinstance(formula, Not):
        if isinstance(formula.inner, Not):
            return remove_double_negation(formula.inner.inner)
        return Not(remove_double_negation(formula.inner))
    if isinstance(formula, And):
        return And(remove_double_negation(formula.left), remove_double_negation(formula.right))
    if isinstance(formula, Or):
        return Or(remove_double_negation(formula.left), remove_double_negation(formula.right))
    return formula

def or_distribuctive(formula):
    if isinstance(formula, Or):
        if isinstance(formula.left, And):
            return And(
                Or(or_distribuctive(formula.left.left), or_distribuctive(formula.right)),
                Or(or_distribuctive(formula.left.right), or_distribuctive(formula.right))
            )
        if isinstance(formula.right, And):
            return And(
                Or(or_distribuctive(formula.left), or_distribuctive(formula.right.left)),
                Or(or_distribuctive(formula.left), or_distribuctive(formula.right.right))
            )
        return Or(or_distribuctive(formula.left), or_distribuctive(formula.right))
    if isinstance(formula, And):
        return And(or_distribuctive(formula.left), or_distribuctive(formula.right))
    return formula

def cnf_direct_transform(formula):
    formula = remove_implies(formula)
    while True:
        last = formula
        formula = de_morgan(formula)
        if formula == last:
            break
    formula = remove_double_negation(formula)
    while not is_cnf(formula):
        formula = or_distribuctive(formula)
    return formula

def get_literals(formula):
    if isinstance(formula, Not):
        return [Not(get_literals(formula.inner)[0])]
    if isinstance(formula, (And, Or, Implies)):
        return get_literals(formula.left) + get_literals(formula.right)
    if is_literal(formula):
        return [formula]
    return []

def cnf_tseitin_transform(formula):
    subforms = subformulas(formula)
    subforms_not_atoms = list(filter(lambda x: not isinstance(x, Atom), subforms))
    for i, subform in enumerate(subforms_not_atoms):
        val = Atom(f'x{i + 1}')
        literals = get_literals(subform)
        ors = Or(Not(val), reduce(lambda x, y: Or(x, y), literals))
        formula = And(formula, ors) if i != 0 else ors
        for literal in literals:
            formula = And(formula, Or(Not(literal), val))
    return cnf_direct_transform(formula)
