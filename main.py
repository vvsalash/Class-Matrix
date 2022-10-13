from sys import stdin
from copy import deepcopy


class MatrixError(Exception):
    def __init__(self, matrix, other):
        self.matrix1 = matrix
        self.matrix2 = other


class Matrix:
    def __init__(self, matrix):
        self.matrix = deepcopy(matrix)

    def __str__(self):
        string = ''
        string += str(self.matrix[0][0])
        for i in range(1, len(self.matrix[0])):
            string += '\t' + str(self.matrix[0][i])
        for i in range(1, len(self.matrix)):
            string += '\n' + str(self.matrix[i][0])
            for j in range(1, len(self.matrix[i])):
                string += '\t' + str(self.matrix[i][j])
        return str(string)

    def size(self):
        size = (len(self.matrix), len(self.matrix[0]))
        return size

    def __add__(self, other):
        if len(self.matrix) == len(other.matrix):
            size = len(self.matrix[0])
            for rows in self.matrix:
                if size != len(rows):
                    raise MatrixError(self, other)
            for rows in other.matrix:
                if size != len(rows):
                    raise MatrixError(self, other)
            string = []
            array = []
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    mat = other.matrix[i][j] + self.matrix[i][j]
                    string.append(mat)
                    if len(string) == len(self.matrix[0]):
                        array.append(string)
                        string = []
            return Matrix(array)
        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            string = []
            array = []
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    mat = other * self.matrix[i][j]
                    string.append(mat)
                array.append(string)
                string = []
        elif isinstance(other, Matrix):
            if len(self.matrix[0]) == len(other.matrix):
                string = []
                array = []
                mat = 0
                for i in range(len(self.matrix)):
                    for k in range(len(other.matrix[0])):
                        for j in range(len(self.matrix[0])):
                            mat += self.matrix[i][j] * other.matrix[j][k]
                        string.append(mat)
                        mat = 0
                    array.append(string)
                    string = []
            else:
                raise MatrixError(self, other)

        return Matrix(array)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(other)
        elif isinstance(other, Matrix):
            if len(self.matrix) == len(other.matrix[0]):
                string = []
                array = []
                mat = 0
                for i in range(len(other.matrix)):
                    for k in range(len(self.matrix[0])):
                        for j in range(len(other.matrix[0])):
                            mat += other.matrix[i][j] * self.matrix[j][k]
                        string.append(mat)
                        mat = 0
                    array.append(string)
                    string = []
            else:
                raise MatrixError(self, other)
        return Matrix(array)

    def transpose(self):
        string = []
        transpose_matrix = []
        for i in range(len(self.matrix[0])):
            for j in range(len(self.matrix)):
                string.append(self.matrix[j][i])
            transpose_matrix.append(string)
            string = []
        self.matrix = transpose_matrix
        return Matrix(transpose_matrix)

    @staticmethod
    def transposed(self):
        string = []
        transpose_matrix = []
        for i in range(len(self.matrix[0])):
            for j in range(len(self.matrix)):
                string.append(self.matrix[j][i])
            transpose_matrix.append(string)
            string = []
        return Matrix(transpose_matrix)

    def add_row(self, i, j, alpha):
        for k in range(len(self.matrix[0])):
            self.matrix[i][k] += self.matrix[j][k] * alpha

    def mul_row(self, i, alpha):
        for k in range(len(self.matrix[0])):
            self.matrix[i][k] *= alpha

    def swap_rows(self, i, j):
        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]

    def solve(self, vector):
        array = []
        for i in range(len(self.matrix)):
            array.append(self.matrix[i] + [vector[i]])
        mat = Matrix(array)
        for i in range(len(self.matrix) - 1):
            row_index = i
            for j in range(i + 1, len(self.matrix)):
                if (mat.matrix[j][i] - mat.matrix[row_index][i]) * (mat.matrix[j][i] + mat.matrix[row_index][i]) > 0:
                    row_index = j
            if not mat.matrix[row_index][i]:
                break
            mat.swap_rows(row_index, i)

            for j in range(i + 1, len(self.matrix)):
                alpha = - mat.matrix[j][i] / mat.matrix[i][i]
                mat.add_row(j, i, alpha)

        # for i in range(len(self.matrix)):
        #     if i < len(self.matrix[0]) - 1:
        #         if not mat.matrix[i][i]:
        #             raise MatrixError(self, mat)
        #     else:
        #         for j in range(len(self.matrix[0])):
        #             if not (mat.matrix[i][j] == 0 and mat.matrix[i][-1] == 0):
        #                 raise MatrixError(self, mat)

        solution = [0] * len(self.matrix[0])

        for i in range(len(self.matrix) - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                mat.add_row(j, i, - (mat.matrix[j][i] / mat.matrix[i][i]))

        for i in range(len(self.matrix)):
            mat.mul_row(i, 1 / mat.matrix[i][i])
            solution[i] = mat.matrix[i][-1]
        return solution


class SquareMatrix(Matrix):
   def square(self):
        if len(self.matrix) == len(self.matrix[0]):
            return Matrix(self.matrix)

   def __pow__(self, power):
       if power == 0:
           mat = [[0] * len(self.matrix) for _ in range(len(self.matrix))]
           for i in range(len(self.matrix)):
               mat[i][i] += 1
           return Matrix(mat)
       elif power == 1:
           return Matrix(self.matrix)
       elif power > 1:
           if power % 2 == 0:
               x = self.__pow__(power // 2)
               return x * x
           elif power % 2 != 0:
               return self.__pow__(power - 1) * self


exec(stdin.read())


