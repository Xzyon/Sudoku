from SudoGenerator import *

# the Sudoku() function generate a uniquely solvable sudoku in the form of a numpy 2D array

my_sudoku1 = Sudoku()

# the Sudoku() function also accept 2 optional arguments :
# full_grid= a full sudoku grid which will be used as template to generate the final sudoku
# missing_value= an integer between 0 and 81, which specify the number of missing of missing values in the grid
#                By default set to 0, it returns a uniquely solvable sudoku with the maximum number of missing values.

full_sudoku = np.array([[9, 4, 5, 2, 3, 7, 6, 8, 1],
                        [3, 1, 7, 9, 6, 8, 2, 5, 4],
                        [6, 8, 2, 1, 5, 4, 3, 7, 9],
                        [2, 3, 1, 4, 7, 5, 8, 9, 6],
                        [4, 5, 6, 3, 8, 9, 1, 2, 7],
                        [7, 9, 8, 6, 1, 2, 4, 3, 5],
                        [1, 2, 3, 5, 9, 6, 7, 4, 8],
                        [5, 7, 4, 8, 2, 1, 9, 6, 3],
                        [8, 6, 9, 7, 4, 3, 5, 1, 2]])

my_sudoku2 = Sudoku(full_grid=full_sudoku,missing_value=50)

# The solve() function require a sudoku grid as argument and return a generator object.
# The generator will then yield one solution per call.

solution_generator2 = solve(grid=my_sudoku2)
print("1st solution :")
solution1 = next(solution_generator2)
print(solution1)
print("2nd solution :")
solution2 = next(solution_generator2)
print(solution2)

# The generator will return a StopIteration error when out of possible solution

solution_generator1 = solve(grid=my_sudoku1)
print("1st and only solution :")
solution1 = next(solution_generator1)
print(solution1)
print("no other solution, return StopIteration error :")
solution2 = next(solution_generator1)