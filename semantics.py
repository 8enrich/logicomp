"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """

from formula import *
from itertools import product

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
