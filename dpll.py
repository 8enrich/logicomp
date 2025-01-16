from formula import Atom, Not, Or, Implies, And
from functions import is_cnf, subformulas
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
        if isinstance(formula.inner, (Or, And)):
            left = de_morgan(formula.inner.left)
            right = de_morgan(formula.inner.right)
            if isinstance(formula.inner, Or):
                return And(Not(left), Not(right))
            if isinstance(formula.inner, And):
                return Or(Not(left), Not(right))
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
            right = or_distribuctive(formula.right)
            return And(
                Or(or_distribuctive(formula.left.left), right),
                Or(or_distribuctive(formula.left.right), right)
            )
        if isinstance(formula.right, And):
            left = or_distribuctive(formula.left)
            return And(
                Or(left, or_distribuctive(formula.right.left)),
                Or(left, or_distribuctive(formula.right.right))
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
    subforms_not_atoms = list(filter(lambda x: not isinstance(x, Atom), subformulas(formula)))
    vals = [Atom(f'x_{i}') for i in range(len(subforms_not_atoms))]
    new_vals = dict(zip(subforms_not_atoms, vals)) 
    print(vals, new_vals)
    clauses = [] 
    def get_clauses(formula):
        if isinstance(formula, Atom):
            return formula
        a = new_vals[formula]
        if isinstance(formula, Not):
            b = get_clauses(formula.inner)
            clauses.append(Or(Not(a), Not(b)))
            clauses.append(Or(b, a))
            return a
        b = get_clauses(formula.left)
        c = get_clauses(formula.right)
        if isinstance(formula, And):
            clauses.append(Or(Not(a), b))
            clauses.append(Or(Not(a), c))
            clauses.append(Or(a, Or(Not(b), Not(c))))
        if isinstance(formula, Or):
            clauses.append(Or(a, Not(b)))
            clauses.append(Or(a, Not(c)))
            clauses.append(Or(Not(a), Or(b, c)))
        return a
    get_clauses(formula)
    new_formula = reduce(lambda x, y: And(x, y), clauses)
    new_formula = And(new_formula, new_vals[formula])
    return new_formula

def cnf_tseitin_transform(formula):
    formula = nnf_transform(formula)
    formula = remove_double_negation(formula)
    return to_cnf(formula) 

formula = Not(And(Atom('p'), Or(Atom('q'), Not(Atom('r'))))) 
print(cnf_tseitin_transform(formula))
