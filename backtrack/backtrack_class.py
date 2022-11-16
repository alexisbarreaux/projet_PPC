# Main file for the backtrack algorithm.
from typing import Callable, Tuple

from models import CSP
from constants import Variable
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
    # Variables for optimisation problems
    optimization_state_evaluation: Callable
    optimization_value_comparison: Callable
    best_known_state: dict
    best_known_value: float

    def __init__(
        self,
        next_variable_choosing_method: Callable = naive_variable_choosing,
        next_values_ordering_method: Callable = naive_values_ordering,
        optimization_state_evaluation: Callable = None,
        optimization_value_comparison: Callable = lambda x, y: x < y,
    ) -> None:
        self.next_variable_choosing_method = next_variable_choosing_method
        self.next_values_ordering_method = next_values_ordering_method
        self.optimization_state_evaluation = optimization_state_evaluation
        self.optimization_value_comparison = optimization_value_comparison
        return

    def check_if_new_state_is_valid(
        self, csp_instance: CSP, state: dict, new_variable: Variable
    ):
        """
        If the previous state was valid, only constraints between the variable which now has a value
        and the previous ones can be violated.
        """
        # At the start, no variable was added and thus no constraint is wrong.
        if new_variable is None:
            return True

        else:
            new_VariableValue = state[new_variable]
            # For each variable (including the new one but this isn't an issue)
            for variable in state.keys():
                # Try to get the constraint, it can be stored either with the key (variable, new_variable) or the
                # (new_variable, variable) one.
                if (
                    constraint_to_check := csp_instance.constraints.get(
                        (variable, new_variable), None
                    )
                ) is not None:
                    # If the constraint exists, see if it holds
                    VariableValue = state[variable]
                    if not (VariableValue, new_VariableValue) in constraint_to_check:
                        return False

                elif (
                    constraint_to_check := csp_instance.constraints.get(
                        (new_variable, variable), None
                    )
                ) is not None:
                    # If the constraint exists, see if it holds
                    VariableValue = state[variable]
                    if not (new_VariableValue, VariableValue) in constraint_to_check:
                        return False
            # At the end if no new constraint is False, then they are all True.
            return True

    def _backtrack(
        self, csp_instance: CSP, state: dict, new_variable: Variable = None
    ) -> Tuple[bool, dict]:
        """
        This is the decision kind. It will return back the first possible solution.
        A backtrack takes a CSP and a current state (variables that currently hold values). We also put the
        last added variable in new_variable because it makes check violations easier.

        The backtrack first checks if the current state is valid, and if not returns False.
        Otherwise it appends a new value for the next variable to the state and moves on recursively.

        The state is depicted as a dict, in which keys are variables names and values the value of
        each variable. A variable which currently holds no value is not in the dict.

        It returns a boolean and the current state.
        """
        # Check if a constraint is invalid
        if not self.check_if_new_state_is_valid(
            csp_instance=csp_instance, state=state, new_variable=new_variable
        ):
            return False, state
        # If the current state is complete (all variables have values), then return it
        if len(state) == len(csp_instance.variables):
            return True, state

        # Otherwise, choose a new variable to add to state
        new_variable = self.next_variable_choosing_method(
            csp_instance=csp_instance, state=state
        )
        # Compute the order in which to test the possible values
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance, new_variable=new_variable
        )

        for new_variable_possible_value in new_variable_values_order:
            # Copy the state dict to be able to call recurisvely without issue
            new_state = state.copy()
            new_state.update({new_variable: new_variable_possible_value})

            child_result, child_state = self._backtrack(
                csp_instance=csp_instance, state=new_state, new_variable=new_variable
            )
            if child_result:
                # If a sub node has a solution, go back up and return true
                return True, child_state

        # If no sub nodes was true, return false
        return False, state

    def run_backtrack(self, csp_instance: CSP) -> Tuple[bool, dict]:
        return self._backtrack(csp_instance=csp_instance, state=dict())

    def _check_if_state_is_better_optimization(self, new_state: dict) -> None:
        """
        When encountering a valid state for an optimization problem,
        store it with this function if it is better than the current one.
        """
        if self.best_known_state is None or self.optimization_value_comparison(
            self.best_known_value,
            (new_value := self.optimization_state_evaluation(new_state)),
        ):
            self.best_known_state = new_state
            self.best_known_value = new_value
        return

    def _reset_optimization_variables(self) -> None:
        self.best_known_value = None
        self.best_known_state = None
        return

    def _backtrack_optimization(
        self, csp_instance: CSP, state: dict, new_variable: Variable = None
    ) -> None:
        """
        This is the optimization kind. It will return back the best possible solution and thus
        explore the tree for a longer time.
        It returns a boolean and the first found optimal state.
        """
        # Check if a constraint is invalid
        if not self.check_if_new_state_is_valid(
            csp_instance=csp_instance, state=state, new_variable=new_variable
        ):
            return
        # If the current state is complete (all variables have values), evaluate it.
        if len(state) == len(csp_instance.variables):
            self._check_if_state_is_better_optimization(new_state=state)
            return

        # Otherwise, choose a new variable to add to state
        new_variable = self.next_variable_choosing_method(
            csp_instance=csp_instance, state=state
        )
        # Compute the order in which to test the possible values
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance, new_variable=new_variable
        )

        for new_variable_possible_value in new_variable_values_order:
            # Copy the state dict to be able to call recurisvely without issue
            new_state = state.copy()
            new_state.update({new_variable: new_variable_possible_value})

            # Don't need to check child as we will be exploring all valid edges.
            self._backtrack_optimization(
                csp_instance=csp_instance, state=new_state, new_variable=new_variable
            )

        return

    def run_optimization_backtrack(self, csp_instance: CSP) -> Tuple[float, dict]:
        """
        Actual function to be called to run a backtrack for an optimization problem.
        """
        self._reset_optimization_variables()
        self._backtrack_optimization(csp_instance=csp_instance, state=dict())
        return self.best_known_value, self.best_known_state
