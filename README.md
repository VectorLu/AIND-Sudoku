# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: <br />
    1. Find all boxes that have two possible digits, add them to a list -- two_digits_boxes. <br />
    2. Compare the boxes in two_digits_boxes with the box in the same unit. If those two box have two digits and the two digits are the same, the peer box is the naked twin of it. Then eliminate these two digits from their peer boxes' values. <br />
    3. Repeat step2 until the possibilities is not reducible.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: <br />
    1. Design the data structure by the diagonal sudoku rubric. <br />
    2. Eliminate possibilities by the determined value. <br />
    3. Use only_choice to determine the value to fill in the box. <br />
    4. If the possibilities are reducible, repeat step2 and step3 util the possibilities is not reducible.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
