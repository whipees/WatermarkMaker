import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
"""
 přidání cesty do seznamu, kde Python hledá moduly
"""
sys.path.append(parent_dir)

from src import main

if __name__ == "__main__":
    main.run_app()