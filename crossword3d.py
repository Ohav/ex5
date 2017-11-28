#############################################################
# FILE : crossword3d.py
# WRITERS : Matan Toledano , matancha , 313591935
#           Ohav Barbi , ohavb , 316019488
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION: A program that gets a letter cube and a list
# of words. It splits the cube into layers of boards,
# according to a given direction and for each board it uses
# the module crossword.py to count how many times each word
# appears in it, in all possible directions.
# Finally, it prints the results to a text file.
#############################################################

import os
import sys
import crossword

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
        original_matrices = [matrix.split('\n') for matrix in
                             matrix_file.read().split('\n***\n')]

    with open(argv[WORD_LIST_LOCATION], 'r') as word_list_file:
        word_list = word_list_file.read().split('\n')

    # We clean the matrix strings
    for matrix in original_matrices:
        for i in range(len(matrix)):
            matrix[i] = matrix[i].split(',')

    word_count_all_matrices = []
    matrices = get_matrices(original_matrices, directions)

    for matrix in matrices:
        configured_matrix = crossword.configure_matrix(
            matrix, crossword.ALL_DIRECTIONS_LIST)
        word_count_list = crossword.count_words_per_direction(
            configured_matrix, word_list)
        word_count_all_matrices += word_count_list

    crossword.write_words_to_output(argv[OUTPUT_LOCATION],
                                    word_count_all_matrices)


def get_matrices(original_matrices, directions):
    """Gets a 'cube' of letters, creates and returns layers (matrix boards)
    made out of it, according to given directions.
    """
    matrices_to_check = []

    # Height and width must be the same for each matrix in the set
    matrix_height = len(original_matrices[0])
    matrix_width = len(original_matrices[0][0])

    for direction in directions:
        if direction == POSSIBLE_DIRECTIONS[0]:
            matrices_to_check += original_matrices
        elif direction == POSSIBLE_DIRECTIONS[1]:
            row_matrices = []
            for i in range(matrix_height):
                row_matrices.append([matrix[i]
                                     for matrix in original_matrices])
            matrices_to_check += row_matrices
        elif direction == POSSIBLE_DIRECTIONS[2]:
            column_matrices = []
            for i in range(matrix_width):
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
