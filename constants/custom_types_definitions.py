from typing import Union, Tuple

variable_value = Union[float, int]
domain = list[variable_value]
constraint = list[Tuple[variable_value, variable_value]]
