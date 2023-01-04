# Main file for the backtrack algorithm.
from typing import Callable, Tuple
from time import time

from models import CSP

from .AC3 import AC3_current_state
from .forward_checking import forward_checking_current_state
from .variables_choosing_algorithms import (
    naive_variable_choosing,
)
from .values_ordering_algorithms import naive_values_ordering
from constants import VariableValue


class BacktrackClass:
    """
    This is a wrapper around the backtrack function in itself to be able to choose
    different methods of selecting next node, value, etc.
    It has the following properties:
        - next_variable_choosing_method (Callable): the function used to select the next variable
            we want to put in the state. It takes the CSP and current state as input. It defaults to the
            naive choice where we just take the next variable in the CSP's order. It also take the current
            domains_last_valid_index.
        - next_values_ordering_method (Callable): the function used to order the values and know in
            which order to test them.. It takes the CSP and new variable as input. It defaults to the
            naive order where we just take the next varaible's domain.
        - optimization_state_evaluation (Callable): a function to choose between two states when working on an optimization
            (and not decision) problem.
        - domains_last_valid_index : this states for i in range the number of variables, which subpart of the domain of
            the variable is currently valid, inspired by the slides of the third lesson on memory management.

    """

    next_variable_choosing_method: Callable
    next_values_ordering_method: Callable
    leaf_evaluation_method: Callable[[dict], bool]
    # Booleans for the added layers of consistency and prospective search
    use_arc_consistency: bool
    use_forward_checking: bool
    arc_consistency_frequency: int
    # Statistics attributes
    nodes: int = 0
    # Variables that need to be reset
    domains_last_valid_index: list[int]
    # Time variables
    time_limit: int
    start_time: float
    run_time: float

    def __init__(
        self,
        next_variable_choosing_method: Callable = naive_variable_choosing,
        next_values_ordering_method: Callable = naive_values_ordering,
        leaf_evaluation_method: Callable = None,
        use_arc_consistency: bool = False,
        use_forward_checking: bool = False,
        arc_consistency_frequency: int = 1,
        time_limit: int = -1,
    ) -> None:
        self.next_variable_choosing_method = next_variable_choosing_method
        self.next_values_ordering_method = next_values_ordering_method
        self.use_arc_consistency = use_arc_consistency
        self.arc_consistency_frequency = arc_consistency_frequency
        self.use_forward_checking = use_forward_checking
        self.time_limit = time_limit
        # By default always return True in a valid leaf
        if leaf_evaluation_method is None:
            self.leaf_evaluation_method = self.decision_leaf_evaluation
        else:
            self.leaf_evaluation_method = leaf_evaluation_method
        return

    def _reset_statistics_variables(self) -> None:
        """
        Used before each backtrack
        """
        self.nodes = 0
        self.start_time = time()
        return

    def _update_runtime(self) -> None:
        self.run_time = time() - self.start_time

    def decision_leaf_evaluation(self, leaf_state: dict) -> bool:
        """
        In a decision problem, being in a leaf is always enough.
        """
        return True

    def _check_if_new_state_is_valid(
        self, csp_instance: CSP, state: dict, last_variable_index: int
    ) -> bool:
        """
        If the previous state was valid, only constraints between the variable which now has a value
        and the previous ones can be violated.
        """
        if last_variable_index is None:
            return True

        last_variable_value = state[last_variable_index]
        for other_variable_index in state:
            other_variable_value = state[other_variable_index]
            if other_variable_index != last_variable_index:
                if (
                    constraint := csp_instance.constraints.get(
                        (last_variable_index, other_variable_index), None
                    )
                ) is not None:
                    if not constraint(
                        last_variable_index,
                        other_variable_index,
                        last_variable_value,
                        other_variable_value,
                    ):
                        # If the constraint was not valid, directly return False
                        return False

        return True

    def _revert_shrinking_operations(
        self, csp_instance: CSP, shrinking_operations: dict
    ) -> None:
        """
        Reset the domain index when backtracking.
        """
        for variable_index in shrinking_operations:
            self.domains_last_valid_index[variable_index] += shrinking_operations[
                variable_index
            ]
        return

    def _revert_last_variable_domain(
        self,
        csp_instance: CSP,
        last_variable_index: int,
        last_variable_domain_first_value: VariableValue,
        last_variable_domain_size: int,
    ) -> None:
        csp_instance.domains[last_variable_index][0] = last_variable_domain_first_value
        self.domains_last_valid_index[last_variable_index] = last_variable_domain_size
        return

    def _backtrack(
        self, csp_instance: CSP, state: dict, last_variable_index: int = None
    ) -> Tuple[bool, dict]:
        """
        This backtrack will return back the first possible solution.
        A backtrack takes a CSP and a current state (variables that currently hold values). We also put the
        last added variable in last_variable because it makes check violations easier.

        The backtrack first checks if the current state is valid, and if not returns False.
        Otherwise it appends a new value for the next variable to the state and moves on recursively.

        The state is depicted as a dict, in which keys are variables idexes and values the value of
        each variable. A variable which currently holds no value is not in the dict.

        It returns a boolean and the current state.
        """
        self.nodes += 1
        # If runtime is exceeded, return with False as we don't know if the node is valid or not.
        self._update_runtime()
        if self.time_limit > 0 and self.run_time >= self.time_limit:
            return False, state

        # Check if a constraint is invalidated by the new state
        if not self._check_if_new_state_is_valid(
            csp_instance=csp_instance,
            state=state,
            last_variable_index=last_variable_index,
        ):
            return False, state

        # If the current state is a leaf, evaluate it
        if len(state) == len(csp_instance.variables):
            return self.leaf_evaluation_method(state), state

        if last_variable_index is not None:
            last_variable_domain_first_value = csp_instance.domains[
                last_variable_index
            ][0]
            last_variable_domain_size = self.domains_last_valid_index[
                last_variable_index
            ]

            last_variable_value = state[last_variable_index]
            csp_instance.domains[last_variable_index][0] = last_variable_value
            self.domains_last_valid_index[last_variable_index] = 0

        shrinking_operations: dict = dict()
        # Use arc consistency if asked
        if (
            self.use_arc_consistency
            and (self.nodes % self.arc_consistency_frequency) == 0
        ):
            emptied_a_domain = AC3_current_state(
                csp_instance=csp_instance,
                state=state,
                shrinking_operations=shrinking_operations,
                domains_last_valid_index=self.domains_last_valid_index,
                last_variable_index=last_variable_index,
            )
            if emptied_a_domain:
                self._revert_shrinking_operations(
                    csp_instance=csp_instance,
                    shrinking_operations=shrinking_operations,
                )
                if last_variable_index is not None:
                    self._revert_last_variable_domain(
                        csp_instance=csp_instance,
                        last_variable_index=last_variable_index,
                        last_variable_domain_first_value=last_variable_domain_first_value,
                        last_variable_domain_size=last_variable_domain_size,
                    )
                return False, state

        # Use forward checking if asked
        if self.use_forward_checking:
            emptied_a_domain = forward_checking_current_state(
                csp_instance=csp_instance,
                state=state,
                last_variable_index=last_variable_index,
                shrinking_operations=shrinking_operations,
                domains_last_valid_index=self.domains_last_valid_index,
            )
            if emptied_a_domain:
                self._revert_shrinking_operations(
                    csp_instance=csp_instance,
                    shrinking_operations=shrinking_operations,
                )
                if last_variable_index is not None:
                    self._revert_last_variable_domain(
                        csp_instance=csp_instance,
                        last_variable_index=last_variable_index,
                        last_variable_domain_first_value=last_variable_domain_first_value,
                        last_variable_domain_size=last_variable_domain_size,
                    )
                return False, state

        # Otherwise, choose a new variable to add to state
        new_variable_index = self.next_variable_choosing_method(
            csp_instance=csp_instance,
            state=state,
            domains_last_valid_index=self.domains_last_valid_index,
        )
        # Compute the order in which to test the possible values
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance,
            last_variable_index=new_variable_index,
            domain_last_valid_index=self.domains_last_valid_index[new_variable_index],
        )

        for new_variable_possible_value in new_variable_values_order:
            state.update({new_variable_index: new_variable_possible_value})

            child_result, child_state = self._backtrack(
                csp_instance=csp_instance,
                state=state,
                last_variable_index=new_variable_index,
            )
            if child_result:
                # If a sub node has a solution, go back up and return true
                return True, child_state

        # If no sub nodes was true, undo domains modifications
        if self.use_forward_checking or self.use_arc_consistency:
            self._revert_shrinking_operations(
                csp_instance=csp_instance, shrinking_operations=shrinking_operations
            )
        if last_variable_index is not None:
            self._revert_last_variable_domain(
                csp_instance=csp_instance,
                last_variable_index=last_variable_index,
                last_variable_domain_first_value=last_variable_domain_first_value,
                last_variable_domain_size=last_variable_domain_size,
            )
        # Remove new index if no successful child was found.
        state.pop(new_variable_index)
        # Then return false
        return False, state

    def run_backtrack(self, csp_instance: CSP) -> Tuple[bool, dict]:
        """
        Runs the backtrack and creates a human readable state to return.
        """
        self._reset_statistics_variables()

        self.domains_last_valid_index = [
            len(csp_instance.domains[i]) - 1 for i in range(len(csp_instance.domains))
        ]

        found_solution, indexes_state = self._backtrack(
            csp_instance=csp_instance, state=dict()
        )
        readable_state = dict()
        for index in indexes_state:
            readable_state[csp_instance.variables[index]] = indexes_state[index]

        return found_solution, readable_state
