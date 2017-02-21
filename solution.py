# coding: utf-8
# Learn from Udacity.
all_digits = '123456789'
rows = 'ABCDEFGHI'
cols = all_digits

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

# A list of units in the same row
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# It is the top most row.
row_units = [cross(r, cols) for r in rows]

# A list of units in the same column
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.
column_units = [cross(rows, c) for c in cols]

# A list of units in the same 3x3 square
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# A list of two main diagonals.
diagonal_units = [
    ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
    ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']
]

# unit_list = row_units + column_units + square_units
unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def find_eliminate_twins(values):
    """
    Find and eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    two_digits_boxes = [box for box in boxes if len(values[box]) == 2]
    for t in two_digits_boxes:
        for unit in units[t]:
            twin = [box for box in unit if values[box] == values[t]]
            twin.remove(t)
            if len(twin) == 1:
                twin_digit = values[twin[0]]
                print
                digit_1 = twin_digit[0]
                digit_2 = twin_digit[1]
                for box in unit:
                    if box == t or box == twin[0]:
                        continue
                    if digit_1 in values[box]:
                        eliminated_twins = values[box].replace(digit_1, '')
                        assign_value(values, box, eliminated_twins)
                    if digit_2 in values[box]:
                        eliminated_twins = values[box].replace(digit_2, '')
                        assign_value(values, box, eliminated_twins)
            else:
                continue

    return values

def naked_twins(values):
    """
    Eliminate as many as possible values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # TODO: Constraint propagation
    reducible = True
    while reducible:
        sum_of_possibilies_before = 0
        sum_of_possibilies_after = 0
        for box in boxes:
            sum_of_possibilies_before += len(values[box])
        find_eliminate_twins(values)
        for box in boxes:
            sum_of_possibilies_after += len(values[box])
        reducible = (sum_of_possibilies_after < sum_of_possibilies_before)
        # Sanity check, return False if there is a box with zero available value:
        if len([box for box in boxes if len(values[box]) == 0]):
            return False

    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    digits = []
    for digit in grid:
        if digit == '.':
            digits.append(all_digits)
        elif digit in all_digits:
            digits.append(digit)
    return dict(zip(boxes, digits))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)
    seperate_line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(seperate_line)
    return

def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value, eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # If a box has only one digit, then the digit is definite.
    definite_box = [box for box in values.keys() if len(values[box]) == 1]
    for box in definite_box:
        digit = values[box]
        for peer in peers[box]:
            new_digits = values[peer].replace(digit, '')
            assign_value(values, peer, new_digits)

    return values



def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for digit in all_digits:
            # If a box contains the digit, add the box to occur_boxes.
            occur_boxes = [box for box in unit if digit in values[box]]
            # If only one box in a unit contains the digit,
            # then this box is the only choice.
            if len(occur_boxes) == 1:
                # values[occur_boxes[0]] = digit
                assign_value(values, occur_boxes[0], digit)

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both function, the sudoku remains the same, return the sudoku.

    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    reducible = True
    while reducible:
        # Check how many boxes have a determined value
        num_of_solved_values_before = len([box for box in boxes if len(values[box]) == 1])
        # Use the Eliminate Strategy and the Only Choice Strategy
        eliminated_sudoku = eliminate(values)
        after_only_choice_sudoku = only_choice(eliminated_sudoku)
        # Check how many boxes have a determined value, to compare
        num_of_solved_values_after = len([box for box in boxes if len(values[box]) == 1])
        # If new values were added, continue the loop.
        reducible = (num_of_solved_values_before != num_of_solved_values_after)
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in boxes if len(values[box]) == 0]):
            return False

    return values

# TODO: assign_value()
def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of unfilled boxes with the fewest possibilities
    n, s = min((len(values[s], s)) for s in boxes if len(values[s]) > 1)

    # Use recursion to solve each one of the Resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for digit in values[s]:
        # Copy the sudoku to protect the original sudoku
        # in case that there is no solution.
        new_sudoku = values.copy()
        # new_sudoku[s] = digit
        assign_value(new_sudoku, s, digit)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    initial_sudoku = grid_values(grid)
    final_sudoku = search(initial_sudoku)

    return final_sudoku



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
