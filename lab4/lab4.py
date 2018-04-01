# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp):
    """Returns True if the problem has one or more empty domains, otherwise False"""
    for var in csp.get_all_variables():
        if not csp.get_domain(var):
            return True
    return False


def check_all_constraints(csp):
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    for var1 in list(csp.assignments.keys()):
        for var2 in list(csp.assignments.keys()):
            if csp.constraints_between(var1, var2) is not None:
                for constraint in csp.constraints_between(var1, var2):
                    if not constraint.check(csp.get_assignment(var1), csp.get_assignment(var2)):
                        return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem):
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    static_eval = 0
    agenda = [problem]

    while agenda:
        p = agenda.pop(0)
        static_eval += 1
        p = p.set_unassigned_vars_order(p.unassigned_vars)
        if has_empty_domains(p) or (not check_all_constraints(p)):
            pass
        else:
            if not p.unassigned_vars:
                return p.assignments, static_eval
            else:
                first_un_var = p.pop_next_unassigned_var()
                new_ps = []
                for val in p.domains.get(first_un_var, None):
                    new_p = p.copy()
                    new_p.set_assignment(first_un_var, val)
                    new_ps.append(new_p)
            agenda = new_ps + agenda

    return None, static_eval


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

# poke_p = get_pokemon_problem()
# print(solve_constraint_dfs(poke_p))

ANSWER_1 = 20


#### Part 3: Forward Checking ##################################################


def any_constraint_violation(csp, var1, var2, val2):
    constraints = csp.constraints_between(var1, var2)
    domain1 = csp.get_domain(var1)
    dict = {}
    for i in range(len(domain1)):
        val1 = domain1[i]
        dict[i] = True
        for j in range(len(constraints)):
            constraint = constraints[j]
            if not constraint.check(val1, val2):
                dict[i] = False

    return True if True in list(dict.values()) else False


def eliminate_from_neighbors(csp, var):
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """

    eliminates = []
    for n_var in csp.get_neighbors(var):
        n_domain = csp.domains[n_var]
        n_domain_copy = n_domain.copy()
        val_vio = False
        for val in n_domain_copy:
            if not any_constraint_violation(csp, var, n_var, val):
                if csp.get_assignment(n_var) is not val:
                    n_domain.remove(val)
                if len(n_domain) == 0:
                    return None
                val_vio = True
        if val_vio:
            eliminates.append(n_var)
    return sorted(eliminates)

# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors


def solve_constraint_forward_checking(problem):
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    static_eval = 0
    agenda = [problem]

    while agenda:
        p = agenda.pop(0)
        static_eval += 1
        p = p.set_unassigned_vars_order(p.unassigned_vars)
        if has_empty_domains(p) or (not check_all_constraints(p)):
            pass
        else:
            if not p.unassigned_vars:
                return p.assignments, static_eval
            else:
                first_un_var = p.pop_next_unassigned_var()
                new_ps = []
                for val in p.domains.get(first_un_var, None):
                    new_p = p.copy()
                    new_p.set_assignment(first_un_var, val)
                    forward_check(new_p, first_un_var)
                    new_ps.append(new_p)
            agenda = new_ps + agenda

    return None, static_eval


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = 9


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None):
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    if queue is None:
        queue = csp.get_all_variables()

    dequeued_list = []

    while queue:
        var = queue.pop(0)
        dequeued_list.append(var)
        fc = forward_check(csp, var)
        if fc is None:
            return None
        else:
            for i in fc:
                if i not in queue:
                    queue.append(i)
    return dequeued_list


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

ANSWER_3 = 6


def solve_constraint_propagate_reduced_domains(problem):
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """
    static_eval = 0
    agenda = [problem]

    while agenda:
        p = agenda.pop(0)
        static_eval += 1
        p = p.set_unassigned_vars_order(p.unassigned_vars)
        if has_empty_domains(p) or (not check_all_constraints(p)):
            pass
        else:
            if not p.unassigned_vars:
                return p.assignments, static_eval
            else:
                first_un_var = p.pop_next_unassigned_var()
                new_ps = []
                for val in p.domains.get(first_un_var, None):
                    new_p = p.copy()
                    new_p.set_assignment(first_un_var, val)
                    domain_reduction(new_p, list(new_p.assignments.keys()))
                    new_ps.append(new_p)
            agenda = new_ps + agenda

    return None, static_eval


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = 7


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None):
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    if queue is None:
        queue = csp.get_all_variables()

    dequeued_list = []

    while queue:
        var = queue.pop(0)
        dequeued_list.append(var)
        fc = forward_check(csp, var)
        if fc is None:
            return None
        else:
            for n in fc:
                if enqueue_condition_fn(p=csp, v=n) and (n not in queue):
                    queue.append(n)
    return dequeued_list


def condition_domain_reduction(csp, var):
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True


def condition_singleton(csp, var):
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return True if len(csp.get_domain(var)) == 1 else False


def condition_forward_checking(csp, var):
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None):
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """

    static_eval = 0
    agenda = [problem]

    while agenda:
        p = agenda.pop(0)
        static_eval += 1
        p = p.set_unassigned_vars_order(p.unassigned_vars)
        if has_empty_domains(p) or (not check_all_constraints(p)):
            pass
        else:
            if not p.unassigned_vars:
                return p.assignments, static_eval
            else:
                first_un_var = p.pop_next_unassigned_var()
                new_ps = []
                for val in p.domains.get(first_un_var, None):
                    new_p = p.copy()
                    new_p.set_assignment(first_un_var, val)
                    if enqueue_condition is not None:
                        propagate(enqueue_condition, new_p, list(new_p.assignments.keys()))
                    new_ps.append(new_p)
            agenda = new_ps + agenda

    return None, static_eval


# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = 8


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n):
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return True if m in [n-1, n+1] or n in [m-1, m+1] else False


def constraint_not_adjacent(m, n):
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not(constraint_adjacent(m, n))


def all_different(variables):
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints, paired = [], []

    for i in variables:
        for j in variables:
            if i != j and [i, j] not in paired:
                constraints.append(Constraint(i, j, constraint_different))
                paired.append([j, i])

    return constraints

#### SURVEY ####################################################################

NAME = 'Tuo Sun'
COLLABORATORS = 'None'
HOW_MANY_HOURS_THIS_LAB_TOOK = 9
WHAT_I_FOUND_INTERESTING = 'Find the difference among all types of search'
WHAT_I_FOUND_BORING = 'None'
SUGGESTIONS = None
