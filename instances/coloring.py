from pathlib import Path

from models import CSP
from .instances_utils import read_instance_edge_line

lambda_wrapper_for_a_couple_of_variables = None


def coloring_optimization_problem(graph_path: Path) -> CSP:
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
        domains = {
            variable: list(range(1, number_of_nodes + 1)) for variable in variables
        }

        csp_coloring = CSP(variables=variables, domains=domains, constraints={})

        # At this point we have built a naive coloring CSP with no constraint.
        # So we now add constraint one by one when we discover the edges.
        for _ in range(number_of_edges):
            _, first_node, second_node = instance_file.readline().split(" ")
            position_of_first_node_variable = int(first_node) - 1
            position_of_second_node_variable = int(second_node) - 1
            _, new_constraint = lambda_wrapper_for_a_couple_of_variables(
                csp_instance=csp_coloring,
                i=position_of_first_node_variable,
                j=position_of_second_node_variable,
                boolean_lambda=(
                    lambda i, j, value_var_i, value_var_j: value_var_i != value_var_j
                ),
            )
            csp_coloring.add_constraint(
                variable_1=first_node,
                variable_2=second_node,
                new_constraint=new_constraint,
            )

        return csp_coloring
