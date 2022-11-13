from constants import domain, constraint


class CSP:
    """
    A CSP is represented in the following way in this project:
        - each variable is a string, in order to be able to have the clearest possible names for them
            instead of only indices (thinking for instance of the problem of Lewis Caroll's zebra where variables
            would be treated easily by giving them the name of the attributes they represented). They are stored in
            a list
        - each domain is a list of the possible values taken. They are stored in a dict since
            our variables are strings.
        - each constraint is a list of tuples of admissibles variables values for the variables
            of the constraint. They are stored in a dict whose key is the tuple (variable_1, variable_2)
            and whose value is the possible values of said variables.

    """

    variables: list[str]
    domains: dict[str, domain]
    constraints: dict[(str, str), constraint]

    def __init__(
        self,
        variables: list[str],
        domains: dict[str, domain],
        constraints: dict[(str, str), constraint],
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
