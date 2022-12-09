import os
from pathlib import Path

# This avoids using getcwd which will be wrong inside a notebook.
COLORING_INSTANCES_PATH = Path(os.path.dirname(__file__))

# Stores name of the file and known optimal value
COLORING_INSTANCES = {
    "anna.col.txt": 11,
    "jean.col.txt": 10,
    "le450_25b.col.txt": 25,
    "myciel3.col.txt": 4,
    "myciel4.col.txt": 5,
    "myciel5.col.txt": 6,
    "myciel6.col.txt": 7,
    "myciel7.col.txt": 8,
    "queen13_13.col.txt": 13,
    "toy_chain.txt": 2,
    "toy_odd_cycle.txt": 3,
    "toy_even_cycle.txt": 2,
    "toy_triangle.txt": 3,
}
