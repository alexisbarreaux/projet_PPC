import os
from pathlib import Path

# This avoids using getcwd which will be wrong inside a notebook.
COLORING_INSTANCES_PATH = Path(os.path.dirname(__file__))

COLORING_INSTANCES = [
    "anna.col.txt",
    "jean.col.txt",
    "le450_25b.col.txt",
    "myciel3.col.txt",
    "myciel4.col.txt",
    "myciel5.col.txt",
    "myciel6.col.txt",
    "myciel7.col.txt",
    "queen13_13.col.txt",
    "toy_chain.txt",
    "toy_cycle.txt",
    "toy_triangle.txt",
]
