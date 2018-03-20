from LinkedMatrix import DataObject, ColumnObject
from Matrix import Matrix


def search(k, h, solution):
    """Dancing links algorithm. For more detail, read the original paper.

    :param int k: Recursion depth
    :param ColumnObject h: Root of LinkedMatrix
    :param List[int] solution: Solution of exact cover
    :return Boolean: Returns True if exact cover exists, False otherwise
    """
    # Choose a column
    c = h.choose()

    # Solution found
    # There no more columns are left to iterate over
    if c == h:
        return True

    # Solution not found
    # There is at least one column, with no more rows left
    if c.D == c:
        return False

    # Cover column c
    c.cover()

    # Set row to iterate over
    r = c.D

    # While selected row is not the column headers
    while r != c:

        # Cover all columns that intersect current row
        r.cover_row()

        # If solution exists, add it
        if search(k + 1, h, solution):
            solution.append(r.row)
            return True

        # Uncover all columns that intersect current row
        r.uncover_row()

        # Move to next row
        r = r.D

    # Uncover column c
    c.uncover()

    return False

def generate_sudoku_col_headers(n):
    """Generate the column headers for a Sudoku puzzle grid of size n**2.
    These headers are to be used in LinkedMatrix.

    :param int n: n**2 is the size of Sudoku puzzle grid.
    :return List[str]: Returns list of strings of column headers.
    """
    if n < 1:
        raise Exception("Invalid grid size!")

    col_headers_to_col_numbers = {}
    col_numbers_to_col_headers = {}

    rows = []
    cols = []
    boxes = []
    row_col = []

    # n**2 numbers
    for i in range(1, n**2 + 1):

        # n**2 possible rows/columns/boxes per number
        for j in range (1, n**2 + 1):

            # Headers for positions
            row_pos = "#" + str(i) + "R" + str(j)
            col_pos = "#" + str(i) + "C" + str(j)
            box_pos = "#" + str(i) + "B" + str(j)

            # Append column headers
            rows.append(row_pos)
            cols.append(col_pos)
            boxes.append(box_pos)

    # n**2 rows
    for i in range(1, n ** 2 + 1):

        # n**2 cols
        for j in range(1, n ** 2 + 1):
            row_col_pos = "R" + str(i) + "C" + str(j)
            row_col.append(row_col_pos)


    # Merge possible headers
    boxes.extend(row_col)
    cols.extend(boxes)
    rows.extend(cols)
    col_headers = rows

    return col_headers

def generate_sudoku_matrix(n):
    """Generate exact cover matrix of Sudoku puzzle with size n**2.

    :param int n: n**2 is size of corresponding Sudoku puzzle grid.
    :return RootObject: The exact cover LinkedMatrix.
    """
    if n < 1:
        raise Exception("Invalid grid size!")

    sudoku_rows = []
    col_headers = generate_sudoku_col_headers(n)
    dicts = generate_sudoku_row_dicts(n)
    row_number_to_position = dicts[0]
    position_to_row_number = dicts[1]

    # Total possible placements of numbers
    num_rows = n**6

    # Total number of columns headers
    num_cols = (n ** 4) * 4

    # Construct matrix row by row
    for i in range(1, num_rows + 1):
        matrix_row = [0] * len(col_headers)
        position = row_number_to_position[i]
        number = position[0:2]

        row = position[2:4]
        matrix_row[col_headers.index(number + row)] = 1

        col = position[4:6]
        matrix_row[col_headers.index(number + col)] = 1

        box_num = convert_row_col_to_box(n, int(row[1]), int(col[1]))
        box = "B"+str(box_num)
        matrix_row[col_headers.index(number + box)] = 1

        row_col = row + col
        matrix_row[col_headers.index(row_col)] = 1

        sudoku_rows.append(matrix_row)

    sudoku_matrix = Matrix(num_rows, num_cols)
    sudoku_matrix.set_matrix(sudoku_rows)
    return sudoku_matrix.convert(col_headers)


def generate_sudoku_row_dicts(n):
    """Generate a dictionary that converts row numbers in exact cover matrix
    that corresponds to a string denoting row, column and number inside
    each square of corresponding Sudoku puzzle grid of size n**2.

    :param int n: n**2 is size of Sudoku puzzle grid.
    :return Dict[int, str]: Dictionary that is returned.
    """
    if n < 1:
        raise Exception("Invalid grid size!")

    row_number_to_position = {}
    row_number = 0

    # n**2 numbers
    for i in range(1, n**2 + 1):

        # n**2 rows
        for j in range(1, n**2 + 1):

            # n**2 columns
            for k in range(1, n**2 + 1):

                row_number += 1
                pos = "#"+str(i)+"R"+str(j)+"C"+str(k)
                row_number_to_position[row_number] = pos

    position_to_row_number = invert(row_number_to_position)

    return row_number_to_position, position_to_row_number


def invert(dictionary):
    """Inverts dict dictionary.

    :param dict dictionary: Dictionary to invert.
    :return dict: Returns inverted dictionary
    """
    inverse_dictionary = {}
    for item in dictionary.items():
        inverse_dictionary[item[1]] = item[0]
    return inverse_dictionary

def convert_row_col_to_box(n, row, col):
    """Given size of Sudoku grid along with the row and column of a single cell,
    the box that cell belongs to is returned. The cell numbers are incremented
    left to right from top row down.

    :param int n: n**2 is size of Sudoku grid.
    :param int row: Row of cell in question.
    :param int col: Column of cell in question.
    :return int: Returns box number of cell in question.
    """
    if row % n != 0:
        row_partition_number = (row // n) + 1
    else:
        row_partition_number = row // n

    if col % n != 0:
        col_partition_number = (col // n) + 1
    else:
        col_partition_number = col // n

    box = n * (row_partition_number - 1) + col_partition_number

    return box
