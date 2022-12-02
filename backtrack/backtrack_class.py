# Main file for the backtrack algorithm.
from typing import Callable, Tuple

from models import CSP

from .AC3 import AC3_current_state
from .forward_checking import forward_checking_current_state
from .variables_choosing_algorithms import naive_variable_choosing
from .values_ordering_algorithms import naive_values_ordering


class BacktrackClass:
    """
    This is a wrapper around the backtrack function in itself to be able to choose
    different methods of selecting next node, value, etc.
    It has the following properties:
        - next_variable_choosing_method (Callable): the function used to select the next variable
            we want to put in the state. It takes the CSP and current state as input. It defaults to the
            naive choice where we just take the next variable in the CSP's order.
        - next_values_ordering_method (Callable): the function used to order the values and know in
            which order to test them.. It takes the CSP and new variable as input. It defaults to the
            naive order where we just take the next varaible's domain.
        - optimization_state_evaluation (Callable): a function to choose between two states when working on an optimization
            (and not decision) problem.

    """

    next_variable_choosing_method: Callable
    next_values_ordering_method: Callable
    leaf_evaluation_method: Callable[[dict], bool]
    # Booleans for the added layers of consistency and prospective search
    use_arc_consistency: bool
    use_forward_checking: bool
    # Statistics attributes
    nodes: int = 0

    def __init__(
        self,
        next_variable_choosing_method: Callable = naive_variable_choosing,
        next_values_ordering_method: Callable = naive_values_ordering,
        leaf_evaluation_method: Callable = None,
        use_arc_consistency: bool = False,
        use_forward_checking: bool = False,
    ) -> None:
        self.next_variable_choosing_method = next_variable_choosing_method
        self.next_values_ordering_method = next_values_ordering_method
        self.use_arc_consistency = use_arc_consistency
        self.use_forward_checking = use_forward_checking
        # By default always return True in a valid leaf
        if leaf_evaluation_method is None:
            self.leaf_evaluation_method = self.decision_leaf_evaluation
        else:
            self.leaf_evaluation_method = leaf_evaluation_method
        return

    def reset_statistics_variables(self) -> None:
        """
        Used before each backtrack
        """
        self.nodes = 0
        return

    def decision_leaf_evaluation(self, leaf_state: dict) -> bool:
        """
        In a decision problem, being in a leaf is always enough.
        """
        return True

    def check_if_new_state_is_valid(
        self, csp_instance: CSP, state: dict, last_variable_index: int
    ) -> bool:
        """
        If the previous state was valid, only constraints between the variable which now has a value
        and the previous ones can be violated.
        """
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

        # If not in the root node
        if not last_variable_index is None:
            # Check if a constraint is invalidated by the new state
            # TODO might not be needed when we use forward checking
            if not self.check_if_new_state_is_valid(
                csp_instance=csp_instance,
                state=state,
                last_variable_index=last_variable_index,
            ):
                return False, state

            # If the current state is a leaf, evaluate it
            if len(state) == len(csp_instance.variables):
                return self.leaf_evaluation_method(state), state
            # Otherwise use forward checking if asked
            elif self.use_forward_checking:
                checking_emptied_domain = forward_checking_current_state(
                    csp_instance=csp_instance,
                    state=state,
                    last_variable_index=last_variable_index,
                )
                # If forward checking empties a domain, return
                if checking_emptied_domain:
                    return False, state

        # Otherwise, choose a new variable to add to state
        last_variable_index = self.next_variable_choosing_method(
            csp_instance=csp_instance, state=state
        )
        # Compute the order in which to test the possible values
        # TODO handle the last variable index here better
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance, last_variable_index=last_variable_index
        )

        if self.use_forward_checking:
            # Store current valid indices for the domains to revert it later when backtracking
            # TODO sub optimal, we now that we will at most modify only the indices of the ones not yet in state.
            current_valid_indices = csp_instance.domains_last_valid_index.copy()

        for new_variable_possible_value in new_variable_values_order:
            # Copy the state dict to be able to call recurisvely without issue
            # TODO this copy could probably be removed by removing last added value in the dict
            # when finding an invalid state.
            new_state = state.copy()
            new_state.update({last_variable_index: new_variable_possible_value})

            child_result, child_state = self._backtrack(
                csp_instance=csp_instance,
                state=new_state,
                last_variable_index=last_variable_index,
            )
            if child_result:
                # If a sub node has a solution, go back up and return true
                return True, child_state
            elif self.use_forward_checking:
                # If the child was not satisfactory, revert what needs to be
                csp_instance.domains_last_valid_index = current_valid_indices.copy()

        # If no sub nodes was true, return false
        return False, state

    def run_backtrack(self, csp_instance: CSP) -> Tuple[bool, dict]:
        """
        Runs the backtrack and creates a human readable state to return.
        """
        self.reset_statistics_variables()

        found_solution, indexes_state = self._backtrack(
            csp_instance=csp_instance, state=dict()
        )
        readable_state = dict()
        for index in indexes_state:
            readable_state[csp_instance.variables[index]] = indexes_state[index]

        return found_solution, readable_state
