import os
from pathlib import Path

# This avoids using getcwd which will be wrong inside a notebook.
SUDOKU_INSTANCES_PATH = Path(os.path.dirname(__file__))

# Stores name of the file and known optimal value
SUDOKU_EASY_INSTANCES = [
    "easy1.txt",
    "easy10.txt",
    "easy2.txt",
    "easy3.txt",
    "easy4.txt",
    "easy5.txt",
    "easy6.txt",
    "easy7.txt",
    "easy8.txt",
    "easy9.txt",
]
SUDOKU_INTERMEDIATE_INSTANCES = [
    "intermediate1.txt",
    "intermediate10.txt",
    "intermediate2.txt",
    "intermediate3.txt",
    "intermediate4.txt",
    "intermediate5.txt",
    "intermediate6.txt",
    "intermediate7.txt",
    "intermediate8.txt",
    "intermediate9.txt",
]
SUDOKU_EXPERT_INSTANCES = [
    "expert1.txt",
    "expert10.txt",
    "expert2.txt",
    "expert3.txt",
    "expert4.txt",
    "expert5.txt",
    "expert6.txt",
    "expert7.txt",
    "expert8.txt",
    "expert9.txt",
]
SUDOKU_ALL_INSTANCES = (
    ["empty.txt"]
    + SUDOKU_EASY_INSTANCES
    + SUDOKU_INTERMEDIATE_INSTANCES
    + SUDOKU_EXPERT_INSTANCES
)
