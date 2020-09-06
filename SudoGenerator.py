import numpy as np
import random

def shuffle(s):
    """ shuffle a list s of number of any length """
    return random.sample(s, len(s))


# INIT
grid = np.zeros([ 9, 9 ], int)
RandomSeq = shuffle(range(1, 10))


def check(grid, y, x, n):
    """ check if number n is present in line y, colummn x and the 3x3 subgrid containing the position [y][x]
            return false if n is found at checked position
            return true if not
    """
    for i in range(0, 9):
        if grid[ y ][ i ] == n: return False
        if grid[ i ][ x ] == n: return False

    x0 = (x // 3) * 3
    y0 = (y // 3) * 3

    for i in range(3):
        for j in range(3):
            if grid[ y0 + i ][ x0 + j ] == n: return False

    return True


def solve(grid):
    """ solve a 9x9 sudoku grid by recursion.
            return a generator object : output should be used with the next() function and return a numpy 2Darray

    In case the sudoku grid contains more than one solution, next() can be called again until all
    solutions are exhausted.
    """
    for y in range(9):
        for x in range(9):
            if grid[ y ][ x ] == 0:
                for n in range(1, 10):
                    if check(grid, y, x, n):
                        grid[ y ][ x ] = n

                        yield from solve(grid)

                        grid[ y ][ x ] = 0
                return
    yield grid


def ManualSudoGen():
    """ Manually generate the first three sub grids and first column of a sudoku grid
        return a 9x9 numpy 2D array

    Empty positions have a value of 0
    Generated positions have a value between 1 and 9
    """

    # enter center coordinate of a 3x3 sub matrix
    #    return the full list of its coordinates
    def submatrix(centerX, centerY):
        return [ [ centerX + a, centerY + b ] for a in range(-1, 2) for b in range(-1, 2) ]

    center = [ [ 1 + a * 3, 1 + b * 3 ] for a in range(3) for b in range(3) ]

    # remove a list of things "b" from another list of things "a"
    #   return a list
    def RemoveList(a, b):
        return list(set(a) - set(b))

    # Generate first sub matrix
    FirstSub = submatrix(center[ 0 ][ 0 ], center[ 0 ][ 1 ])
    for n in range(9):
        grid[ FirstSub[ n ][ 0 ] ][ FirstSub[ n ][ 1 ] ] = RandomSeq[ n ]

    # Generate second sub matrix
    SecondSub = submatrix(center[ 1 ][ 0 ], center[ 1 ][ 1 ])

    row1 = shuffle(RandomSeq[ 3:9 ])
    row2 = shuffle(RandomSeq[ 0:3 ] + RandomSeq[ 6:9 ])
    row3 = shuffle(RandomSeq[ 0:6 ])

    for n in range(3):
        if row1[ n ] in row2:
            row2.remove(row1[ n ])
        if row1[ n ] in row3:
            row3.remove(row1[ n ])
        if len(row3) > 3:
            if row2[ n ] in row1:
                row1.remove(row2[ n ])
            if row2[ n ] in row3:
                row3.remove(row2[ n ])
        elif len(row3) == 3:
            for i in range(3):
                if row3[ i ] in row1:
                    row1.remove(row3[ i ])
                if row3[ i ] in row2:
                    row2.remove(row3[ i ])

    if len(row3) < 3:
        if not row2[ -1 ] in row3:
            row3.append(row2[ -1 ])
        elif not row2[ -2 ] in row3:
            row3.append(row2[ -2 ])

    row1 = row1[ :3 ]
    row2 = row2[ :3 ]
    row3 = row3[ :3 ]

    for n in range(3):
        grid[ SecondSub[ n ][ 0 ] ][ SecondSub[ n ][ 1 ] ] = row1[ n ]
        grid[ SecondSub[ n + 3 ][ 0 ] ][ SecondSub[ n + 3 ][ 1 ] ] = row2[ n ]
        grid[ SecondSub[ n + 6 ][ 0 ] ][ SecondSub[ n + 6 ][ 1 ] ] = row3[ n ]

    # Generate third sub matrix
    ThirdSub = submatrix(center[ 2 ][ 0 ], center[ 2 ][ 1 ])

    row1 = shuffle(RemoveList(RandomSeq, grid[ 0 ]))
    row2 = shuffle(RemoveList(RandomSeq, grid[ 1 ]))
    row3 = shuffle(RemoveList(RandomSeq, grid[ 2 ]))

    for n in range(3):
        grid[ ThirdSub[ n ][ 0 ] ][ ThirdSub[ n ][ 1 ] ] = row1[ n ]
        grid[ ThirdSub[ n + 3 ][ 0 ] ][ ThirdSub[ n + 3 ][ 1 ] ] = row2[ n ]
        grid[ ThirdSub[ n + 6 ][ 0 ] ][ ThirdSub[ n + 6 ][ 1 ] ] = row3[ n ]

    # Generate first column

    col1 = shuffle(RemoveList(RandomSeq, grid.T[ 0 ]))

    for n in range(6):
        grid.T[ 0 ][ n + 3 ] = col1[ n ]

    return grid


# generate a half sudoku grid manually
half_grid = ManualSudoGen()
# solve it by recursion to get a full grid
gen_full_grid = solve(grid=half_grid)
full_grid = next(gen_full_grid)


def Sudoku(full_grid=full_grid, missing_value=0):

    """
From a full sudoku grid, generate a Sudoku grid with missing values.

optional arguments:
    full_grid = numpy 2D array filled with integers (1 to 9) and no empty position (0). If not specified, a random grid is
                used as the template to generate the final sudoku grid.
    missing_value = int ( 1 to 81 ). Specify the number of empty position needed, consequently may or may not return a
                    uniquely solvable sudoku.
                    special value: 0 will return a uniquely solvable sudoku with the maximum number of empty position
                    possible (Default)


    Empty positions have a value of 0
    Generated positions have a value between 1 and 9
    """
    if missing_value < 0 or missing_value > 81:
        raise ValueError("missing_value should be between 0 and 81")

    nb_empty = np.ndarray.sum(np.isin(full_grid, 0))
    if nb_empty != 0 :
        raise ValueError("grid has %s empty position, and should not !" % nb_empty)

    single_index = shuffle(range(81))
    optional_counter = 0

    for i in single_index:
        cache_grid = full_grid.copy()
        full_grid[ np.unravel_index(single_index[ i ], full_grid.shape) ] = 0

        solution = solve(grid=full_grid)

        yield_counter = 0
        optional_counter += 1

        while True:
            try:
                next(solution)
                yield_counter += 1

            except StopIteration:
                break

        if missing_value == 0 and yield_counter > 1:
            print("A uniquely solvable sudoku:")
            print(cache_grid)
            return cache_grid
        if missing_value == optional_counter:
            print("A solvable sudoku with %d missing value and %d solution:" % (missing_value, yield_counter))
            print(full_grid)
            return full_grid
