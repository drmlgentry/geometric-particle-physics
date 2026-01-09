# check_packages.py
import numpy as np
import mpmath as mp
import matplotlib
import sys

print("Python version:", sys.version)
print("NumPy version:", np.__version__)
print("mpmath version:", mp.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("\n✓ All packages installed successfully!")