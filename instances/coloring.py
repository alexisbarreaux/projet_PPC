from typing import Tuple

from pathlib import Path

from models import CSP
from backtrack import BacktrackClass

lambda_wrapper_for_a_couple_of_variables = None


def coloring_problem(graph_path: Path) -> CSP:
    """
    Used to build a CSP to be resolved as an optimization problem to color a graph.
    """
    with open(graph_path, "r") as instance_file:
        while (line := instance_file.readline()).startswith("c"):
            pass

        splitted_line = line.split(" ")
        number_of_nodes, number_of_edges = int(splitted_line[2]), int(splitted_line[3])
        # We could build smarter domains but won't
        variables = [str(i) for i in range(1, number_of_nodes + 1)]
        # Domains are left empty and will be computed in the optimization function
        domains = [[] for _ in range(len(variables))]

        csp_coloring = CSP(variables=variables, domains=domains, constraints={})

        # At this point we have built a naive coloring CSP with no constraint.
        # So we now add constraint one by one when we discover the edges.
        for _ in range(number_of_edges):
            _, first_node, second_node = instance_file.readline().split(" ")
            first_node_index = int(first_node) - 1
            second_node_index = int(second_node) - 1
            csp_coloring.add_constraint(
                index_variable_1=first_node_index,
                index_variable_2=second_node_index,
                new_constraint=lambda i, j, value_var_i, value_var_j: value_var_i
                != value_var_j,
            )

        return csp_coloring


def state_colors_count(state: dict) -> int:
    """
    Counts the number of different colors used in a state
    of the backtrack.
    """
    # Get the colors and create a set to remove duplicates
    colors = set(list(state.values()))
    return len(colors)


def coloring_optimization(
    coloring_instance: CSP,
    use_arc_consistency: bool = False,
    use_forward_checking: bool = False,
) -> Tuple[int, bool, int]:
    """
    This function takes a coloring problem instance and returns an upper bound
    (if not the minimum) number of colors needed to color this graph, the best state and
    the number of nodes in the best state.
    """
    # For now it is very naive, we test the colorings between 2 colors and n colors
    # by dichotomy to know the optimal value.
    n = len(coloring_instance.variables)
    # Result variables
    best_coloring_size = n
    best_state = None
    best_nodes = None
    # Process variables
    smallest_size_to_test = 1
    backtrack_object = BacktrackClass(
        use_arc_consistency=use_arc_consistency,
        use_forward_checking=use_forward_checking,
    )

    while smallest_size_to_test <= best_coloring_size - 1:
        # Split the interval yet to be tested in two, this takes the lower integer part
        size_to_test = int((best_coloring_size + smallest_size_to_test) / 2)

        # One car reduce the domains because of the size constraint.
        for i in range(len(coloring_instance.domains)):
            coloring_instance.domains[i] = [j for j in range(size_to_test)]
        result, state = backtrack_object.run_backtrack(csp_instance=coloring_instance)

        # If it didn't succeed, update smallest_size_to_test
        if not result:
            # Check if we still have sufficient gap
            if best_coloring_size - smallest_size_to_test > 1:
                smallest_size_to_test = size_to_test
            else:
                # Else close the gap and next loop start will be false
                smallest_size_to_test += 1
        # Otherwise update best result and biggest_size_to_test
        else:
            best_coloring_size = size_to_test
            best_state = state
            best_nodes = backtrack_object.nodes

    return best_coloring_size, best_state, best_nodes
