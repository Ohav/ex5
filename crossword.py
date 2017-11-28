import os
import sys

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
POSSIBLE_DIRECTIONS = {'horizontal': ['u', 'd'], 'vertical': ['l', 'r'],
                       'dia_bot_left': ['z', 'w'], 'dia_top_left': ['x', 'y']
                       }


def substr_occurrences(string, sub):
    """Returns the number of occurrences of a substr in a given string
    """
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count += 1
        else:
            return count


def get_word_to_count(matrix, word_list, reverse=False):
    """For each word in the list, searches it in the matrix and returns a
    word-count dictionary
    """
    word_to_count = {}
    for word in word_list:
        for row_string in matrix:
            occurrences = 0
            if reverse is True:
                occurrences += substr_occurrences(row_string, word[::-1])
            else:
                occurrences += substr_occurrences(row_string, word)
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
        conf_mat_list.append(([''.join([mat[j][i] for j in range(len(mat))])
                               for i in range(len(mat[0]))],
                              fitting_directions))

    # Left Right
    if any(direction in POSSIBLE_DIRECTIONS['vertical']
           for direction in directions):
        fitting_directions = get_fitting_directions('vertical', directions)
        # Our matrix is already organized to search rtl or ltr!
        conf_mat_list.append(([''.join([mat[i][j] for j in range(len(mat[i]))])
                               for i in range(len(mat))],
                              fitting_directions))

    # Diagonal bottom left to top right (bottom = 0)
    if any(direction in POSSIBLE_DIRECTIONS['dia_bot_left']
           for direction in directions):
        fitting_directions = get_fitting_directions('dia_bot_left', directions)
        top_to_right = [''.join([mat[i - j][j]
                                 for j in range(len(mat[i]))
                                 if 0 <= i - j < len(mat)])
                        for i in range(len(mat))]
        top_to_right.extend([''.join([mat[-j - 1][i + j + 1]
                                      for j in range(len(mat[i]))
                                      if j + 1 <= len(mat)
                                      and j + i + 1 < len(mat[i])])
                             for i in range(len(mat))])
        conf_mat_list.append((top_to_right, fitting_directions))
    # Diagonal top left to bottom right (bottom = 0)

    if any(direction in POSSIBLE_DIRECTIONS['dia_top_left']
           for direction in directions):
        fitting_directions = get_fitting_directions('dia_top_left', directions)
        left_to_bottom = [''.join([mat[i + j][j]
                                   for j in range(len(mat[i]))
                                   if i + j < len(mat)])
                          for i in range(len(mat))]
        # We're missing half the values
        left_to_bottom.extend([''.join([mat[j][i + j]
                                        for j in range(len(mat[i]))
                                        if i + j < len(mat[i])])
                               for i in range(1, len(mat))])
        conf_mat_list.append((left_to_bottom, fitting_directions))
    return conf_mat_list


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
    possible_directions = ''.join([''.join(POSSIBLE_DIRECTIONS[general_direction])
                                   for general_direction in POSSIBLE_DIRECTIONS])
    for direction in arg_list[DIRECTIONS_LOCATION]:
            if direction not in possible_directions:
                print(ERROR_INVALID_DIRECTION)
                return False
    return True


def combine_dictionary_list(dict_list):
    if not dict_list:
        return None

    main_dict = dict_list[0]
    for i in range(1, len(dict_list)):
        for value in dict_list[i]:
            main_dict[value] = main_dict.get(value, 0) + dict_list[i][value]
    return main_dict


def count_words_per_direction(matrix_list, word_list):
    word_counts = []
    for matrix in matrix_list:
        for direction in matrix[1]:
            if direction in POSSIBLE_DIRECTIONS['horizontal']:
                word_counts.append(get_word_to_count(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['horizontal'][0]))
            elif direction in POSSIBLE_DIRECTIONS['vertical']:
                word_counts.append(get_word_to_count(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['vertical'][0]))
            elif direction in POSSIBLE_DIRECTIONS['dia_top_left']:
                word_counts.append(get_word_to_count(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['dia_top_left'][0]))
            elif direction in POSSIBLE_DIRECTIONS['dia_bot_left']:
                word_counts.append(get_word_to_count(
                    matrix[0], word_list,
                    direction == POSSIBLE_DIRECTIONS['dia_bot_left'][0]))
    return word_counts


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
