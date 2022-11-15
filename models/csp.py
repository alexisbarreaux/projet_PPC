from constants import Domains, Constraints, Variable, Variables, Constraint


class CSP:
    """
    A CSP is represented in the following way in this project:
        - each variable is a string, in order to be able to have the clearest possible names for them
            instead of only indices (thinking for instance of the problem of Lewis Caroll's zebra where variables
            would be treated easily by giving them the name of the attributes they represented). They are stored in
            a list
        - each domain is a list of the possible values taken. They are stored in a dict since
            our variables are strings.
        - each constraint is a set of tuples of admissibles variables values for the variables
            of the constraint. They are stored in a dict whose key is the tuple (variable_1, variable_2)
            and whose value is the possible values of said variables.

    """

    variables: Variables
    domains: Domains
    constraints: Constraints

    def __init__(
        self,
        variables: Variables,
        domains: Domains,
        constraints: Constraints,
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def __str__(self):
        """
        Used to modify display. This string is the one seen when using print(my_csp_instance)
        """
        str_representation = f"Variables:\n{self.variables}\n"

        str_representation += "\nDomains:\n"
        for variable, domain in self.domains.items():
            str_representation += f"{variable} : {domain}\n"

        str_representation += "\nConstraints:\n"
        for var_tuple, constraint in self.constraints.items():
            str_representation += f"{var_tuple} : {constraint}\n"

        return str_representation

    def add_constraint(
        self, variable_1: Variable, variable_2: Variable, new_constraint: Constraint
    ) -> None:
        """
        Add a single constraint to the CSP. If no constraint exists on the variables, just put
        it in the dict. Else, intersect with current constraint.
        """
        # Test first possible order
        if (
            current_constraint := self.constraints.get((variable_1, variable_2), None)
        ) is not None:
            # If the current one exist, intersect current and new.
            self.constraints[
                (variable_1, variable_2)
            ] = current_constraint.intersection(new_constraint)
        # Then second order
        elif (
            current_constraint := self.constraints.get((variable_2, variable_1), None)
        ) is not None:
            # If the current one exist, intersect current and new.
            self.constraints[
                (variable_2, variable_1)
            ] = current_constraint.intersection(new_constraint)
        else:
            # If no current constraint exists, then just put the new constraint as is.
            self.constraints[(variable_1, variable_2)] = new_constraint

        return

    def add_constraints(self, new_constraints: dict) -> None:
        """
        Adds a new bunch of constraints stored as a dict in the CSP.
        """
        for (variable_1, variable_2), constraint in new_constraints.items():
            self.add_constraint(
                variable_1=variable_1, variable_2=variable_2, new_constraint=constraint
            )
        return
