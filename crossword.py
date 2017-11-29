#############################################################
# FILE : crossword.py
# WRITERS : Matan Toledano , matancha , 313591935
#           Ohav Barbi , ohavb , 316019488
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION: A program that gets a crossword board (matrix)
# and a list of words and counts how many times each word
# appears on the board, according to a given direction
# Finally, it prints the results to a text file.
#############################################################

import os
import sys

NUMBER_OF_ARGUMENTS = 5
ERROR_MISSING_ARGUMENTS = "ERROR: Invalid number of parameters. Please " \
                          "enter word_file matrix_file output_file directions."
WORD_LIST_LOCATION = 1
ERROR_MISSING_WORDS = "ERROR: Word file {0} does not exist."
MATRIX_LOCATION = 2
ERROR_MISSING_MATRIX = "ERROR: Matrix file {0} does not exist."
OUTPUT_LOCATION = 3
DIRECTIONS_LOCATION = 4
ERROR_INVALID_DIRECTION = "ERROR: invalid directions."
POSSIBLE_DIRECTIONS = {'horizontal': ['u', 'd'], 'vertical': ['l', 'r'],
                       'dia_bot_left': ['z', 'w'], 'dia_top_left': ['x', 'y']
                       }
ALL_DIRECTIONS_LIST = ''.join([''.join(POSSIBLE_DIRECTIONS[general_direction])
                               for general_direction in POSSIBLE_DIRECTIONS])


def substr_occurrences(string, sub):
    """Returns the number of occurrences of a sub-string in a given string"""
    count = start = 0
    sub = sub.lower()
    while True:
        # Find returns the index of the string, or -1 if nothing was found
        # If we get anything but -1, we know a string was found. We count it,
        # go one forward and check again.
        start = string.find(sub, start) + 1
        if start > 0:
            # Means word was found
            count += 1
        else:
            return count


def count_words_in_board(matrix, word_list, reverse):
    """For each word in the list, searches it in the matrix and returns a
    word-count dictionary
    """
    word_to_count = {}
    for word in word_list:
        # We don't care about the case of the letters in the word.
        # However, at the output file we want to keep the original way the word
        # was written, so we don't change 'word'.
        word_to_check = word.lower()
        for row_string in matrix:
            occurrences = 0
            if reverse is True:
                occurrences += substr_occurrences(row_string,
                                                  word_to_check[::-1])
            else:
                occurrences += substr_occurrences(row_string, word_to_check)
            if occurrences > 0:
                word_to_count[word] = word_to_count.get(word, 0) + occurrences
    return word_to_count


def get_fitting_directions(type, directions):
    """Gets a list of direction and a general direction, and returns which of
    the components that belong to the general direction are in the directions
    """
    fitting_directions = ''
    for direction in POSSIBLE_DIRECTIONS[type]:
        if direction in directions:
            fitting_directions += direction
    return fitting_directions


def configure_matrix(mat, directions):
    """Gets a base matrix and what direction we need to search in.
    Returns a new matrix, configured according to the search direction."""
    conf_mat_list = []
    # Up Down
    if any(direction in POSSIBLE_DIRECTIONS['horizontal']
           for direction in directions):
        fitting_directions = get_fitting_directions('horizontal', directions)
        conf_mat_list.append(([''.join([mat[j][i].lower()
                                        for j in range(len(mat))])
                               for i in range(len(mat[0]))],
                              fitting_directions))

    # Left Right
    if any(direction in POSSIBLE_DIRECTIONS['vertical']
           for direction in directions):
        fitting_directions = get_fitting_directions('vertical', directions)
        # Our matrix is already organized to search rtl or ltr!
        conf_mat_list.append(([''.join([mat[i][j].lower()
                                        for j in range(len(mat[i]))])
                               for i in range(len(mat))],
                              fitting_directions))

    # Diagonal bottom left to top right (bottom = 0)
    if any(direction in POSSIBLE_DIRECTIONS['dia_bot_left']
           for direction in directions):
        fitting_directions = get_fitting_directions('dia_bot_left', directions)
        top_to_right = [''.join([mat[i - j][j].lower()
                                 for j in range(len(mat[i]))
                                 if 0 <= i - j < len(mat)])
                        for i in range(len(mat))]
        # We're missing half the values
        top_to_right.extend([''.join([mat[-j - 1][i + j + 1].lower()
                                      for j in range(len(mat[i]))
                                      if j + 1 <= len(mat)
                                      and j + i + 1 < len(mat[i])])
                             for i in range(len(mat))])
        conf_mat_list.append((top_to_right, fitting_directions))

    # Diagonal top left to bottom right (bottom = 0)
    if any(direction in POSSIBLE_DIRECTIONS['dia_top_left']
           for direction in directions):
        fitting_directions = get_fitting_directions('dia_top_left', directions)
        left_to_bottom = [''.join([mat[i + j][j].lower()
                                   for j in range(len(mat[i]))
                                   if i + j < len(mat)])
                          for i in range(len(mat))]
        # We're missing half the values
        left_to_bottom.extend([''.join([mat[j][i + j].lower()
                                        for j in range(len(mat[i]))
                                        if i + j < len(mat[i])])
                               for i in range(1, len(mat))])
        conf_mat_list.append((left_to_bottom, fitting_directions))
    return conf_mat_list


def combine_dictionary_list(dict_list):
    """Gets a list of counter-dictionaries and returns a combined dictionary"""
    if not dict_list:
        return None

    main_dict = dict_list[0]
    for i in range(1, len(dict_list)):
        for value in dict_list[i]:
            main_dict[value] = main_dict.get(value, 0) + dict_list[i][value]
    return main_dict


def count_words_per_direction(matrix_list, word_list):
    """Gets a list of matrices and a word list, and counts how many time each
    word appears in all of the matrices together.
    """
    word_counts = []
    for matrix in matrix_list:
        for direction in matrix[1]:
            if direction in POSSIBLE_DIRECTIONS['horizontal']:
                word_counts.append(count_words_in_board(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['horizontal'][0]))
            elif direction in POSSIBLE_DIRECTIONS['vertical']:
                word_counts.append(count_words_in_board(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['vertical'][0]))
            elif direction in POSSIBLE_DIRECTIONS['dia_top_left']:
                word_counts.append(count_words_in_board(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['dia_top_left'][0]))
            elif direction in POSSIBLE_DIRECTIONS['dia_bot_left']:
                word_counts.append(count_words_in_board(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['dia_bot_left'][0]))
    return word_counts


def check_args(arg_list, possible_directions=ALL_DIRECTIONS_LIST):
    """Checks if the arguments received by the user are valid."""
    if len(arg_list) != NUMBER_OF_ARGUMENTS:
        print(ERROR_MISSING_ARGUMENTS)
        return False
    if not (os.path.isfile(arg_list[WORD_LIST_LOCATION])):
        print(ERROR_MISSING_WORDS.format(arg_list[WORD_LIST_LOCATION]))
        return False
    elif not(os.path.isfile(arg_list[MATRIX_LOCATION])):
        print(ERROR_MISSING_MATRIX.format(arg_list[MATRIX_LOCATION]))
        return False
    for direction in arg_list[DIRECTIONS_LOCATION]:
            if direction not in possible_directions:
                print(ERROR_INVALID_DIRECTION)
                return False
    return True


def main(argv):
    """Main part of the program, loads the arguments into files and executes
    the main logic.
    """
    if not check_args(argv):
        return
    with open(argv[MATRIX_LOCATION], 'r') as matrix_file:
        matrix = matrix_file.read().split('\n')
    for i in range(len(matrix)):
        matrix[i] = matrix[i].split(',')

    with open(argv[WORD_LIST_LOCATION], 'r') as word_list_file:
        word_list = word_list_file.read().split('\n')

    directions = argv[DIRECTIONS_LOCATION]
    configured_matrix = configure_matrix(matrix, directions)
    word_count_list = count_words_per_direction(configured_matrix, word_list)
    write_words_to_output(argv[OUTPUT_LOCATION], word_count_list)


def write_words_to_output(file_name, word_count_list):
    """Gets a output file name and a list of counter-dictionaries, each with
    it's own count of words.
    The method writes the combined word count onto the file, alphabetically.
    """
    with open(file_name, 'w') as output_file:
        final_word_count = combine_dictionary_list(word_count_list)
        dict_keys = list(final_word_count.keys())
        dict_keys.sort()
        for index, word in enumerate(dict_keys):
            if index != len(dict_keys) - 1:
                output_file.write('{0},{1}\n'
                                  .format(word, final_word_count[word]))
            else:
                output_file.write('{0},{1}'
                                  .format(word, final_word_count[word]))


if __name__ == "__main__":
    main(sys.argv)
