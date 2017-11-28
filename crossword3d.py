import os
import sys
import crossword
import copy

NUMBER_OF_ARGUMENTS = 5
ERROR_MISSING_ARGUMENTS = "ERROR: Invalid number of parameters. Please enter" \
                           "word_file matrix_file output_file directions."
WORD_LIST_LOCATION = 1
ERROR_MISSING_WORDS = "ERROR: Word file word_list.txt does not exist."
MATRIX_LOCATION = 2
ERROR_MISSING_MATRIX = "ERROR: Matrix file mat.txt does not exist."
OUTPUT_LOCATION = 3
DIRECTIONS_LOCATION = 4
ERROR_INVALID_DIRECTION = "ERROR: invalid directions."
POSSIBLE_DIRECTIONS = ['a', 'b', 'c']


def check_args(arg_list):
    """Checks if the arguments received by the user are valid."""
    if len(arg_list) != NUMBER_OF_ARGUMENTS:
        print(ERROR_MISSING_ARGUMENTS)
        return False
    if not (os.path.isfile(arg_list[WORD_LIST_LOCATION])):
        print(ERROR_MISSING_WORDS)
        return False
    elif not(os.path.isfile(arg_list[MATRIX_LOCATION])):
        print(ERROR_MISSING_MATRIX)
        return False
    for direction in arg_list[DIRECTIONS_LOCATION]:
            if direction not in POSSIBLE_DIRECTIONS:
                print(ERROR_INVALID_DIRECTION)
                return False
    return True


def main(argv):
    """Main part of the program, loads the arguments into files and executes
    the main logic.
    """
    if not check_args(argv):
        return
    directions = argv[DIRECTIONS_LOCATION]
    with open(argv[MATRIX_LOCATION], 'r') as matrix_file:
        matrices = get_matrices(matrix_file, directions)

    with open(argv[WORD_LIST_LOCATION], 'r') as word_list_file:
        word_list = word_list_file.read().split('\n')

    word_count_all_matrices = []
    for matrix in matrices:
        configured_matrix = crossword.configure_matrix(matrix, crossword.ALL_DIRECTIONS_LIST)
        word_count_list = crossword.count_words_per_direction(configured_matrix, word_list)
        word_count_all_matrices += word_count_list

    crossword.write_words_to_output(argv[OUTPUT_LOCATION], word_count_all_matrices)


def get_matrices(matrix_file, directions):
    matrices_to_check = []
    original_matrices = [matrix.split('\n') for matrix in matrix_file.read().split('\n***\n')]

    for matrix in original_matrices:
        for i in range(len(matrix)):
            matrix[i] = matrix[i].split(',')

    matrix_height = len(original_matrices[0])
    matrix_length = len(original_matrices[0][0])

    if 'a' in directions:
        matrices_to_check += original_matrices
    if 'b' in directions:
        row_matrices = []
        for i in range(matrix_height):
            row_matrices += [[matrix[i] for matrix in original_matrices]]
        matrices_to_check += row_matrices
    if 'c' in directions:
        column_matrices = []
        for i in range(matrix_length):
            column_matrix = []
            for matrix in original_matrices:
                matrix_line = []
                for line in matrix:
                    matrix_line.append(line[i])
                column_matrix += [matrix_line]
            column_matrices += [column_matrix]
        matrices_to_check += column_matrices

    return matrices_to_check


if __name__ == "__main__":
    main(sys.argv)
