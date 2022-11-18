from typing import Union, Tuple, Callable

# Variables
Variable = str
Variables = list[str]
VariableValue = Union[float, int]

# domains
Domain = list[VariableValue]
# The domains are now just a list of domains are the keys would be the index of the associated variable.
Domains = list[Domain]

# constraints
# A constraint is now a Callable that takes for values, the indices of the two variables to test on and the two
# associated values.
Constraint = Callable[[int, int, VariableValue, VariableValue], bool]
# Constraints are stored in a dict whose keys are the tuple of the indices i and j of the variable it constricts
Constraints = dict[Tuple[int, int], Constraint]
