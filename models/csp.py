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
            and whose value is the lambda function. We ensure we always have index_variable_1 < index_variable_2 for the
            stored constraints.

    When building the CSP we also create a dict which maps variables (as strings) to their index in the list. This is used
    to provide easier functions where one would for instance build a constraint on "Apple" and "Pear" rather than 1 and 14.
    """

    variables_to_index_dict: dict
    variables: Variables
    domains: Domains
    constraints: Constraints

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
        self.variables_to_index_dict = {
            variables[index]: index for index in range(len(variables))
        }

    def build_tuples_from_constraint(
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
            str_representation += f"{(self.variables[i], self.variables[j])}  {self.build_tuples_from_constraint(i, j, constraint)}.\n"

        return str_representation

    def get_current_constraint_if_exists(
        self, index_variable_1: int, index_variable_2: int
    ) -> Constraint:
        """
        Returns the current constraint if it exists, None otherwise.
        """
        return self.constraints.get((index_variable_1, index_variable_2), None)

    def swap_indices_if_needed(
        self,
        index_variable_1: int,
        index_variable_2: int,
        new_constraint: Constraint,
    ) -> Tuple[int, int, Constraint]:
        """
        We want to have and keep index_variable_1 < index_variable_2. Swap them and rebuild the
        constraint.
        """
        # If needed, swap
        if index_variable_1 > index_variable_2:
            swapped_constraint: Constraint = (
                lambda i, j, value_var_i, value_var_j: new_constraint(
                    j, i, value_var_j, value_var_i
                )
            )
            return (index_variable_2, index_variable_1, swapped_constraint)
        else:
            return index_variable_1, index_variable_2, new_constraint

    def combine_two_constraints(
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
        # Get the indices in the right order if not already the case
        (
            index_variable_1,
            index_variable_2,
            new_constraint,
        ) = self.swap_indices_if_needed(
            index_variable_1=index_variable_1,
            index_variable_2=index_variable_2,
            new_constraint=new_constraint,
        )
        # Get current constraint if it exists.
        if (
            current_constraint := self.get_current_constraint_if_exists(
                index_variable_1=index_variable_1, index_variable_2=index_variable_2
            )
        ) is not None:
            # If the current one exists, make a logical "and" with the new one.
            self.constraints[
                (index_variable_1, index_variable_2)
            ] = self.combine_two_constraints(
                current_constraint=current_constraint, new_constraint=new_constraint
            )
        else:
            # If no current constraint exists, then just put the new constraint as is.
            self.constraints[(index_variable_1, index_variable_2)] = new_constraint

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

    # Backtrack functions
    def get_linked_constraints(
        self, variable_index: int
    ) -> list[Tuple[(bool, int, Constraint)]]:
        """
        This function returns the constraints linked to a variable in a list of tuples, the first
        element is a boolean saying wether the index given as an argument is the first of the key,
        the second is the index of the linked variable and the last is the constraint itself.
        So basically:
            (is_variable_index_first, other_index, constraint)
        """
        linked_constraints = []
        # Check variables Var_i with i smaller
        for other_index in range(variable_index):
            if (
                constraint := self.constraints.get((other_index, variable_index), None)
            ) is not None:
                linked_constraints.append((False, other_index, constraint))
        # And then check the bigger ones
        for other_index in range(variable_index + 1, len(self.variables)):
            if (
                constraint := self.constraints.get((other_index, variable_index), None)
            ) is not None:
                linked_constraints.append((True, other_index, constraint))

        return linked_constraints
