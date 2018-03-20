from LinkedMatrix import DataObject, ColumnObject, RootObject

class Matrix:
    """A matrix with integer entries.

    :param int num_rows: Number of rows in this matrix.
    :param int num_cols: Number of columns in this matrix.
    :param List[List[int]] matrix: The matrix is represented by a nested List of ints.
    """

    def __init__(self, num_rows, num_cols):
        """Initialize empty Matrix self.

        :param int num_rows: Number of rows for this matrix.
        :param int num_cols: Number columns for this matrix.
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.matrix = []
        row = []
        for i in range(0, num_cols):
            row.append(0)
        for i in range(0, num_rows):
            self.matrix.append(row.copy())
        self.max_element_size = 1

    def get_row(self, row):
        """Get row number row from Matrix self.

        :param int row: Row number to get.
        :return List[int]: Row of Matrix.
        """
        if row > self.num_rows or row <= 0:
            raise Exception("Row out of bounds!")
        return self.matrix[row - 1]

    def get_col(self, col):
        """Get column number row from Matrix self.

        :param int col: Column number to get.
        :return List[int]: Column of Matrix.
        """
        if col > self.num_cols or col <= 0:
            raise Exception("Column out of bounds!")
        column = []
        for i in range(0, self.num_rows):
            column.append(self.matrix[i][col - 1])
        return column


    def __str__(self):
        """Return str representation of Matrix self.

        :return str: String representation of Matrix.
        """
        content = ""
        for i in range(0, self.num_rows):
            next_row = ""
            for j in range(0, self.num_cols):
                element = self.get(i + 1, j + 1)
                space = (self.max_element_size - element.__str__().__len__()) * " "
                next_row += element.__str__() + space + " "
            content += "\n| " + next_row + "|"
        row_size = int(len(content.split("\n")[1])) - 4
        brace = "--" + row_size * " " + "--"
        return brace + content + "\n" + brace

    def set(self, element, row, col):
        """Set the entry at row row and column col to element.

        :param int element: What the entry should be set to.
        :param int row: Row of entry.
        :param int col: Column of entry.
        :return: None
        """
        self.matrix[row - 1][col - 1] = element
        element_size = element.__str__().__len__()
        if element_size > self.max_element_size:
            self.max_element_size = element_size


    def get(self, row, col):
        """Returns the entry at row row and column col.

        :param int row: Row of entry.
        :param col: Column of entry.
        :return: Returns entry.
        """
        return self.matrix[row - 1][col - 1]

    def remove_row(self, row):
        """Remove row row from Matrix self.

        :param int row: Row to remove
        :return: None
        """
        if row > self.num_rows or row <= 0:
            raise Exception("Row out of bounds!")
        else:
            self.num_rows -= 1
            return self.matrix.pop(row - 1)

    def remove_col(self, col):
        """Remove column col from Matrix self.

        :param int col: Column to remove
        :return: None
        """
        if col > self.num_cols or col <= 0:
            raise Exception("Column out of bounds!")
        else:
            self.num_cols -= 1
            removed_col = []
            for row in self.matrix:
                removed_col.append(row.pop(col - 1))
            return removed_col

    def set_matrix(self, rows):
        """Set the entries in Matrix self based on matrix representation in rows.

        :param List[List[int]] rows: Matrix representation of entries.
        :return: None
        """
        if self.num_rows != len(rows):
            raise Exception("Number of rows do not match!")

        for row in rows:
            if self.num_cols != len(row):
                raise Exception("Number of columns do not match!")

        self.matrix = rows.copy()
        for i in range(0, self.num_rows):
            for j in range(0, self.num_cols):
                element_size = self.get(i + 1, j + 1).__str__().__len__()
                if element_size > self.max_element_size:
                    self.max_element_size = element_size

    def is_boolean(self):
        """Returns whether Matrix self is a boolean matrix (all entries are either 0 or 1).

        :return bool: Whether Matrix self is a boolean matrix.
        """
        for row in self.matrix:
            row_set = set(row)
            if len(row_set) == 0:
                return False
            elif len(row_set) == 1:
                if 0 not in row_set and 1 not in row_set:
                    return False
            elif len(row_set) == 2:
                if 0 not in row_set or 1 not in row_set:
                    return False
            else:
                return False
        return True

    def convert(self, col_headers):
        """Convert Matrix self to a linked matrix, with column headers from col_headers.

        :param List[str] col_headers: Column headers.
        :return RootObject: Returns converted linked matrix.
        """
        if len(col_headers) != self.num_cols:
            raise Exception("Incorrect header number")
        if not self.is_boolean():
            raise Exception("Cannot convert a non-boolean matrix!")
        else:
            root = RootObject(None, None, None, None, None)
            root.L = root
            root.R = root
            curr = root
            for i in range(0, len(col_headers)):
                new = ColumnObject(curr, root, None, None, None, col_headers[i])
                new.U = new
                new.D = new
                curr.R = new
                curr = curr.R

            root.L = curr
            row_count = 0

            #Iterate over rows
            for row in self.matrix:
                row_count += 1
                curr_col = root
                row_LR = None
                row_start = None

                #Iterate over elements in row
                for i in range(0, self.num_cols):
                    curr_col = curr_col.R

                    #If element is a 1
                    if row[i] == 1:
                        col_UD = curr_col

                        #Move down the matrix to the last row
                        while col_UD.D != curr_col:
                            col_UD = col_UD.D

                        #If the row is already under construction
                        if row_LR is not None:
                            row_LR.R = DataObject(row_LR, row_start, col_UD, curr_col, curr_col, row_count)
                            row_LR = row_LR.R

                        #If not, start the construction
                        else:
                            row_start = DataObject(None, None, col_UD, curr_col, curr_col, row_count)
                            row_start.R = row_start
                            row_start.L = row_start
                            row_LR = row_start
                        col_UD.D = row_LR
                        row_LR.C.U = row_LR
                        curr_col.S += 1

                        row_start.L = row_LR
                root.row_headers.append(row_start)

            return root
