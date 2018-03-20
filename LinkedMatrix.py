class DataObject:
    """A node in a linked matrix.
    :param DataObject L: Left node
    :param DataObject R: Right node
    :param DataObject U: Up node
    :param DataObject D: Down node
    :param ColumnObject C: Head of column this node belongs to
    :param int row: Row this node belongs to
    """

    def __init__(self, L, R, U, D, C, row):
        """
        Initialize DataObject.
        :param DataObject L: Left node
        :param DataObject R: Right node
        :param DataObject U: Up node
        :param DataObject D: Down node
        :param ColumnObject C: Head of column this node belongs to
        :param int row: Row this node belongs to
        """
        self.L = L
        self.R = R
        self.U = U
        self.D = D
        self.C = C
        self.row = row

    def cover_row(self):
        """
        Cover the row this node belongs to.
        :return: None
        """
        if self.row != 0:
            c = self.R
            while c != self:
                c.C.cover()
                c = c.R
        else:
            raise Exception("Cannot cover row for column header!")

    def uncover_row(self):
        """
        Uncover the row this node belongs to.
        :return: None
        """
        if self.row!= 0:
            c = self.L
            while c != self:
                c.C.uncover()
                c = c.L
        else:
            raise Exception("Cannot cover row for column header!")

class ColumnObject(DataObject):
    """A column node in a linked matrix, which is the head of a column.
    :param int S: Size of this column.
    :param str N: Name of this column.
    """

    def __init__(self, L, R, U, D, C, N):
        """
        Initialize ColumnObject.
        :param DataObject L: Left node
        :param DataObject R: Right node
        :param DataObject U: Up node
        :param DataObject D: Down node
        :param ColumnObject C: Head of column this node belongs to
        :param str N: Name of this column
        """
        DataObject.__init__(self, L, R, U, D, C, 0)
        self.S = 0
        self.N = N

    def cover(self):
        """
        Cover this column.
        :return: None
        """
        self.R.L = self.L
        self.L.R = self.R
        i = self.D
        while i != self:
            j = i.R
            while j != i:
                j.D.U = j.U
                j.U.D = j.D
                j.C.S = j.C.S - 1
                j = j.R
            i = i.D

    def uncover(self):
        """
        Uncover this column
        :return: None
        """
        i = self.U
        while i != self:
            j = i.L
            while j != i:
                j.C.S = j.C.S + 1
                j.D.U = j
                j.U.D = j
                j = j.L
            i = i.U
        self.R.L = self
        self.L.R = self

    def choose(self):
        """
        Choose the next column to cover with minimum branching factor.
        :return: Next ColumnObject to cover
        """
        c = self
        s = float("inf")
        j = self.R
        while j != self:
            if j.S < s:
                c = j
                s = j.S
            j = j.R
        return c

class RootObject(DataObject):
    """
    RootObject, which is the root or start of linked matrix.
    :param List[int] row_headers: Headers of rows
    """
    def __init__(self, L, R, U, D, C):
        """
        Initialize RootObject
        :param ColumnObject L: Left node
        :param ColumnObject R: Right node
        :param DataObject U: Up node
        :param DataObject D: Down node
        :param ColumnObject C: Head of column this node belongs to
        """
        DataObject.__init__(self, L, R, U, D, C, 0)
        self.row_headers = [0]

    def choose(self):
        """
        Choose the next column to cover with minimum branching factor.
        :return: Next ColumnObject to cover
        """
        c = self
        s = float("inf")
        j = self.R
        while j != self:
            if j.S < s:
                c = j
                s = j.S
            j = j.R
        return c
