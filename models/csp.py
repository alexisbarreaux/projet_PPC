from typing import Tuple

from constants import (
    Domains,
    Constraints,
    Variable,
    Variables,
    Constraint,
    VariableValue,
)


class CSP:
    """
    A CSP is represented in the following way in this project:
        - each variable is a string, in order to be able to have the clearest possible names for them
            instead of only indices (thinking for instance of the problem of Lewis Caroll's zebra where variables
            would be treated easily by giving them the name of the attributes they represented). They are stored in
            a list
        - domains are stored in a list, domains[i] being the domain of the variable C_i.
        - each constraint is a lambda function to evaluate the values of two variables and know wether they are
            valid or not. They are stored in a dict whose key is the tuple (index_variable_1, index_variable_2)
            and whose value is the lambda function. We ensure we always have both (index_variable_1, index_variable_2) and
            (index_variable_2, index_variable_1) at once.

    When building the CSP we also create :
        - variables_to_index_dict : a dict which maps variables (as strings) to their index in the list. This is used
            to provide easier functions where one would for instance build a constraint on "Apple" and "Pear" rather than 1
            and 14.
        - variable_is_constrained_by : a dict which stores for each variables what variables it is constrained by.
    """

    # Init/provided variables
    variables: Variables
    domains: Domains
    constraints: Constraints
    # Built variables
    variables_to_index_dict: dict
    variable_is_constrained_by: dict = None

    # Building functions
    def __init__(
        self,
        variables: Variables,
        domains: Domains,
        constraints: Constraints,
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        # Self built variables
        self.variables_to_index_dict = {
            variables[index]: index for index in range(len(variables))
        }
        self._update_constrained_information_with_constraints(constraints=constraints)
        self.reset_needed_variables()

    def _update_constrained_information_with_single_constraint(
        self, index_variable_1: int, index_variable_2: int
    ) -> None:
        """
        Update data to say that x is now constrained by y and y by x.
        """
        # Create the variable if it doesn't already exist
        if self.variable_is_constrained_by is None:
            self.variable_is_constrained_by = {
                variable_index: set() for variable_index in range(len(self.variables))
            }

        self.variable_is_constrained_by[index_variable_1].add(index_variable_2)
        self.variable_is_constrained_by[index_variable_2].add(index_variable_1)
        return

    def _update_constrained_information_with_constraints(
        self, constraints: Constraints
    ) -> None:
        """
        Update data to know who is constrained by whom.
        """
        for (
            index_variable_1,
            index_variable_2,
        ) in constraints.keys():
            self._update_constrained_information_with_single_constraint(
                index_variable_1=index_variable_1,
                index_variable_2=index_variable_2,
            )

    def _build_tuples_from_constraint(
        self, index_variable_1: int, index_variable_2: int, constraint: Constraint
    ) -> list[Tuple[VariableValue, VariableValue]]:
        return [
            (value_var_1, value_var_2)
            for value_var_1 in self.domains[index_variable_1]
            for value_var_2 in self.domains[index_variable_2]
            if constraint(index_variable_1, index_variable_2, value_var_1, value_var_2)
        ]

    def __str__(self):
        """
        Used to modify display. This string is the one seen when using print(my_csp_instance)
        """
        str_representation = f"Variables:\n{self.variables}\n"

        str_representation += "\nDomains:\n"
        for index in range(len(self.variables)):
            str_representation += f"{self.variables[index]} : {self.domains[index]}\n"

        str_representation += "\nConstraints:\n"
        for (i, j), constraint in self.constraints.items():
            str_representation += f"{(self.variables[i], self.variables[j])}  {self._build_tuples_from_constraint(i, j, constraint)}.\n"

        return str_representation

    def _swap_constraint(
        self,
        constraint: Constraint,
    ) -> Constraint:
        """
        We swap a constraint so that it takes the variables in the opposite order.
        """
        return lambda i, j, value_var_i, value_var_j: constraint(
            j, i, value_var_j, value_var_i
        )

    def _combine_two_constraints(
        self, current_constraint: Constraint, new_constraint: Constraint
    ) -> Constraint:
        """
        This function combines two constraint on the same variables to build a new one.
        """
        return lambda i, j, value_var_i, value_var_j: current_constraint(
            i, j, value_var_i, value_var_j
        ) and new_constraint(i, j, value_var_i, value_var_j)

    def add_constraint(
        self,
        index_variable_1: Variable,
        index_variable_2: Variable,
        new_constraint: Constraint,
    ) -> None:
        """
        Add a single constraint to the CSP. If no constraint exists on the variables, just put
        it in the dict. Else, intersect with current constraint.
        """

        # Store the fact that it possibly adds a constraint (in two orders) that weren't there before
        self._update_constrained_information_with_single_constraint(
            index_variable_1=index_variable_1, index_variable_2=index_variable_2
        )

        # Also get the swapped version of the constraint.
        swapped_constraint = self._swap_constraint(
            constraint=new_constraint,
        )
        # Get the current constraints if they exist.
        if (
            current_constraint := self.constraints.get(
                (index_variable_1, index_variable_2), None
            )
        ) is not None:
            # If the current one exists, make a logical "and" with the new one.
            self.constraints[
                (index_variable_1, index_variable_2)
            ] = self._combine_two_constraints(
                current_constraint=current_constraint, new_constraint=new_constraint
            )
            # If this one exists then the second too, so update it too
            current_constraint = self.constraints.get(
                (index_variable_2, index_variable_1)
            )
            self.constraints[
                (index_variable_2, index_variable_1)
            ] = self._combine_two_constraints(
                current_constraint=current_constraint, new_constraint=swapped_constraint
            )
        else:
            # If no current constraint exists, then just put the new constraint and her swapped
            # version as is.
            self.constraints[(index_variable_1, index_variable_2)] = new_constraint
            self.constraints[(index_variable_2, index_variable_1)] = swapped_constraint

        return

    def add_constraints_with_indices(self, new_constraints: dict) -> None:
        """
        Adds a new bunch of constraints stored as a dict in the CSP. The keys are indices.
        """
        for (index_variable_1, index_variable_2), constraint in new_constraints.items():
            self.add_constraint(
                index_variable_1=index_variable_1,
                index_variable_2=index_variable_2,
                new_constraint=constraint,
            )
        return

    def add_constraint_with_variables(self, new_constraints: dict) -> None:
        """
        Adds a new bunch of constraints stored as a dict in the CSP. The keys are variables.
        """
        for (variable_1, variable_2), constraint in new_constraints.items():
            index_variable_1 = self.variables_to_index_dict[variable_1]
            index_variable_2 = self.variables_to_index_dict[variable_2]
            self.add_constraint(
                index_variable_1=index_variable_1,
                index_variable_2=index_variable_2,
                new_constraint=constraint,
            )
        return
