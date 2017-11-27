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
                       'diag_bot_left': ['w', 'x'], 'diag_top_left': ['y', 'z']
                       }


def substr_occurrences(string, sub):
    """
    Returns the number of occurrences of a substr in a given string
    """
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count += 1
        else:
            return count


def get_word_to_count(matrix, word_list, reverse=False):
    """
    For each word in the list, searches it in the matrix and returns a word-count dictionary
    """
    word_to_count = {}
    for word in word_list:
        for row_string in matrix:
            occurrences = 0

            if reverse is True:
                occurrences += substr_occurrences(row_string[::-1], word)

            occurrences += substr_occurrences(row_string, word)
            if occurrences > 0:
                word_to_count[word] = word_to_count.get(word, 0) + occurrences

    return word_to_count


def split_matrix(mat, directions):
    possible_mat_list = []
    # Up Down
    if any(direction in POSSIBLE_DIRECTIONS['horizontal']
           for direction in directions):
        possible_mat_list.append([[mat[j][i] for j in range(len(mat))]
                                  for i in range(len(mat[0]))])
    # Left Right
    if any(direction in POSSIBLE_DIRECTIONS['vertical']
           for direction in directions):
        # Our matrix is already organized to search rtl or ltr!
        possible_mat_list.append(mat)
    # Diagonal bottom left to top right (bottom = 0)
    if any(direction in POSSIBLE_DIRECTIONS['diag_bot_left']
           for direction in directions):
        top_to_right = [[mat[i - j][j] for j in range(len(mat[i]))
                         if 0 <= i - j < len(mat)]
                        for i in range(len(mat))]
        top_to_right.extend([[mat[-j - 1][i + j + 1]
                              for j in range(len(mat[i]))
                              if j + 1 <= len(mat) and j + i + 1 < len(mat[i])]
                             for i in range(len(mat))])
        possible_mat_list.append(top_to_right)
    # Diagonal top left to bottom right (bottom = 0)
    if any(direction in POSSIBLE_DIRECTIONS['diag_top_left']
           for direction in directions):
        left_to_bottom = [[mat[i + j][j] for j in range(len(mat[i]))
                           if i + j < len(mat)] for i in range(len(mat))]
        # We're missing half the values
        left_to_bottom.extend([[mat[j][i + j] for j in range(len(mat[i]))
                                if i + j < len(mat[i])]
                               for i in range(1, len(mat))])
        possible_mat_list.append(left_to_bottom)


def check_args(arg_list):
    """Checks if the arguments received by the user are valid."""
    print("Arguments received: " + str(arg_list))
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
        if str(direction) not in POSSIBLE_DIRECTIONS:
            print(ERROR_INVALID_DIRECTION)
            return False
    print('all good')
    return True


def main(argv):
    split_matrix('a', 'udlr')
    """Main part of the program, loads the arguments into files and executes
    the main logic.
    """
    if not check_args(argv):
        return
    matrix_file = open(argv[MATRIX_LOCATION], 'r')
    matrix = matrix_file.read().split('\n')
    matrix_file.close()
    print('Matrix: ' + str(matrix))
    word_file = open(argv[WORD_LIST_LOCATION], 'r')
    word_list = word_file.read().split('\n')
    word_file.close()
    print('List: ' + str(word_list))


if __name__ == "__main__":
    main(sys.argv)
