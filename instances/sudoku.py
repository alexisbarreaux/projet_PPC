from typing import Tuple

from pathlib import Path

from models import CSP
from wrappers import alldiff

lambda_wrapper_for_a_couple_of_variables = None


def display_grid(state: dict, grid_edge_size: int = 9) -> list:
    """
    Used to display the resutl of a backtrack on a sudoku instance.
    """
    sudoku_grid = []
    for i in range(grid_edge_size):
        sudoku_grid.append(
            [state[i * grid_edge_size + j] for j in range(grid_edge_size)]
        )
    print(sudoku_grid)
    return sudoku_grid


def sudoku_problem(instance_path: Path, block_edge_size: int = 3) -> Tuple[CSP]:
    """
    Used to build a CSP to be resolved for a sudoku. Returns the built CSP.
    The block length is the size of the corner of one of the subsquares of the
    grid. For instance a 9x9 grid has 9 blocks of size 3x3 and block length = 3.
    """
    grid_edge_size = block_edge_size * block_edge_size

    variables = [
        f"x_{i}_{j}"
        for i in range(1, grid_edge_size + 1)
        for j in range(1, grid_edge_size + 1)
    ]
    # Each variable can take values from 1 to grid size
    domains = [[] for _ in range(len(variables))]

    # Attempt to fill domains up with given file
    with open(instance_path, "r") as instance_file:
        for i in range(grid_edge_size):
            if not (line := instance_file.readline()):
                raise Exception("Missing lines for instance " + instance_path)

            # Each line consists of grid_edge_size ints one after the other
            for j in range(grid_edge_size):
                sudoku_starting_value = int(line[j])
                if sudoku_starting_value != 0:
                    domains[i * grid_edge_size + j] = [sudoku_starting_value]

    # Then fill remaining ones
    for i in range(len(domains)):
        if len(domains[i]) == 0:
            domains[i] = [j for j in range(1, grid_edge_size + 1)]

    # Constraints on rows
    constraints = dict()
    # For each row
    for row_index in range(grid_edge_size):
        first_of_row = row_index * grid_edge_size
        # For each cell
        for i in range(grid_edge_size):
            # For each further cell
            current_cell = first_of_row + i
            for j in range(i + 1, grid_edge_size):
                other_cell = first_of_row + j
                constraints.update(
                    {
                        (current_cell, other_cell): alldiff,
                        (other_cell, current_cell): alldiff,
                    }
                )

    # Constraints on columns
    # For each column
    for column_index in range(grid_edge_size):
        first_of_column = column_index
        # For each cell
        for i in range(grid_edge_size):
            current_cell = first_of_column + i * grid_edge_size
            # For each further cell
            for j in range(i + 1, grid_edge_size):
                other_cell = first_of_column + j * grid_edge_size
                constraints.update(
                    {
                        (current_cell, other_cell): alldiff,
                        (other_cell, current_cell): alldiff,
                    }
                )

    # Constraints on blocks
    for block_top in range(block_edge_size):
        for block_left in range(block_edge_size):
            block_start = block_top * grid_edge_size + block_left
            for i in range(grid_edge_size):
                current_cell = block_start + (i // block_edge_size) * grid_edge_size + i
                for j in range(i + 1, grid_edge_size):
                    current_cell = (
                        block_start + (j // block_edge_size) * grid_edge_size + j
                    )
                    # Here we might have already added a constraint for the pair (i,j)
                    if constraints.get((current_cell, other_cell)) is None:
                        constraints.update(
                            {
                                (current_cell, other_cell): alldiff,
                                (other_cell, current_cell): alldiff,
                            }
                        )

    return CSP(variables=variables, domains=domains, constraints=constraints)
