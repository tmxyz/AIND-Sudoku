# Import required libraries
import re

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Create new units for diagonal sudoku added constaint
diagonal_units = [
    [rows[i] + cols[i] for i in range(0, len(rows))],
    [rows[i] + cols[len(cols) - i - 1] for i in range(0, len(rows))]
]
# Add the diagonal units to the unitlist
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    raise NotImplementedError

    for unit in unitlist:
        # potential_twins are all boxes with 2 potential values, since twins must have two values
        potential_twins = [
            values[box] for box in unit if len(values[box]) == 2
        ]
        # remove all values from potentia_twins, which do not appear twice in the potential_twins list
        twins = [
            twin for twin in potential_twins if potential_twins.count(twin) == 2
        ]
        # check to make sure that we have exactly two potential twins
        if (len(twins) == 2):
            # take the first value as they are identical
            twin = twins[0]
            for box in unit:
                # do not touch the twins themselves and boxes which do not have any potential values, which are in the twins
                if values[box] != twin and re.search(r'[{}]'.format(twin), values[box]):
                    assign_value(values, box, re.sub(
                        r'[{}]'.format(twin), '', values[box])
                    )
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) +
                      ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) is 1]
    for box in solved_values:
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(values[box], ''))
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # apply eliminate strategy
        values = eliminate(values)
        # apply only_choice strategy
        values = only_choice(values)
        # apply naked_twins strategy
        values = naked_twins(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1]
        )
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s)
               for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # create values from the grid and pass them to the search function
    return search(grid_values(grid))


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
