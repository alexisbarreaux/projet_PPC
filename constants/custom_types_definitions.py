from typing import Union, Tuple

# Variables
Variable = str
Variables = list[str]
VariableValue = Union[float, int]
# domains
Domain = list[VariableValue]
Domains = dict[Variable, Domain]
# Variables
Constraint = set[Tuple[VariableValue, VariableValue]]
Constraints = dict[Tuple[Variable, Variable], Constraint]
