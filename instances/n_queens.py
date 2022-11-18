from models import CSP

from wrappers import alldiff


def n_queens_problem(n: int) -> CSP:
    """
    This problem checks wether one can place n queens
    on an nxn grid.
    """
    # This can only be defined on an int.
    assert n > 0 and type(n) == int
    # The i-th variable is the indice of the colonne in which
    # the queen on row i stands.
    # The way our CSP is coded, one will have to get the domain and constraints
    # by checking if a string is a key of a dict. So we put the part that changes
    # from a queen to the next first, in order to check more quickly
    variables = [f"{str(i)}_col_queen" for i in range(1, n + 1)]
    # Each domain is [1, ..., n]
    domains = [list(range(1, n + 1)) for _ in range(len(variables))]

    csp_queen = CSP(variables=variables, domains=domains, constraints={})

    # Constraint Var_i != Var_j
    csp_queen.add_constraints_with_indices(
        {
            (i, j): alldiff
            for i in range(len(variables))
            for j in range(i + 1, len(variables))
        }
    )
    # Constraint : for all i < j,  Var_i - Var_j != j - i
    constraint_1 = (
        lambda i, j, value_var_i, value_var_j: (value_var_i - value_var_j) != j - i
    )
    csp_queen.add_constraints_with_indices(
        {
            (i, j): constraint_1
            for i in range(len(variables))
            for j in range(i + 1, len(variables))
        }
    )
    # Constraint : for all i < j,  Var_j - Var_i != j - i
    constraint_2 = (
        lambda i, j, value_var_i, value_var_j: (value_var_j - value_var_i) != j - i
    )
    csp_queen.add_constraints_with_indices(
        {
            (i, j): constraint_2
            for i in range(len(variables))
            for j in range(i + 1, len(variables))
        }
    )

    return csp_queen
