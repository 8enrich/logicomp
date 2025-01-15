from formula import Atom, Not, Or, Implies, And
from functions import is_cnf
from functools import reduce

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

def nnf_transform(formula):
    formula = remove_implies(formula)
    while True:
        last = formula
        formula = de_morgan(formula)
        if formula == last:
            break
    return formula

def cnf_direct_transform(formula):
    formula = nnf_transform(formula)
    formula = remove_double_negation(formula)
    while not is_cnf(formula):
        formula = or_distribuctive(formula)
    return formula

def to_cnf(formula):
    new_vals = {}
    clauses = set()
    num = 1
    def get_clauses(formula):
        nonlocal num
        if isinstance(formula, Atom):
            return formula
        new_val = new_vals.get(formula)
        if not new_val:
            new_vals[formula] = Atom(f'p_{num}')
            num += 1
        new_val = new_vals.get(formula)
        if isinstance(formula, Not):
            b = get_clauses(formula.inner)
            clauses.add(Or(Not(new_val), Not(b)))
            clauses.add(Or(b, new_val))
        if isinstance(formula, (And, Or)):
            left = get_clauses(formula.left)
            right = get_clauses(formula.right)
            if isinstance(formula, And):
                clauses.add(Or(Not(new_val), left))
                clauses.add(Or(Not(new_val), right))
                clauses.add(Or(new_val, Or(Not(left), Not(right))))
            if isinstance(formula, Or):
                clauses.add(Or(new_val, Not(left)))
                clauses.add(Or(new_val, Not(right)))
                clauses.add(Or(Not(new_val), Or(left, right)))
        return new_val
    get_clauses(formula)
    new_formula = new_vals[formula]
    new_formula = reduce(lambda x, y: And(x, y), clauses)
    return new_formula

def cnf_tseitin_transform(formula):
    formula = nnf_transform(formula)
    formula = remove_double_negation(formula)
    return to_cnf(formula) 
