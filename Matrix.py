import random
import math


class Matrix:
    def __init__(self, rows=1, columns=1):
        self.rows = rows
        self.columns = columns
        self.matrix = [[0 for _ in range(self.rows)] for _ in range(self.columns)]

    def __str__(self):
        r = "["
        for i in self.matrix[:-1]:
            r += f"{i},\n"
        return r + f"{self.matrix[-1]}]"

    def double_array_to_matrix(self, m):
        self.matrix = m
        self.columns = len(m)
        self.rows = len(m[0])
        return self.matrix

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def multi(self, n):
        self.matrix = [[self.matrix[j][i] * n for i in range(self.rows)] for j in range(self.columns)]

    def __dot(self, first, second):
        n, m = first.columns, first.rows

        m, k = second.columns, second.rows

        mtrx = [[0]*k for _ in range(n)]

        for i in range(n):
            for j in range(k):
                for r in range(m):
                    mtrx[i][j] += first.matrix[i][r] * second.matrix[r][j]

        result = Matrix(rows=k, columns=n)
        result.matrix = mtrx
        return result

    # help me
    def __mul__(self, other):
        result = self.__dot(self, other)
        return result

    def randomize(self):
        self.matrix = [[random.uniform(-1, 1) for i in range(self.rows)] for j in range(self.columns)]

    def add(self, n):
        self.matrix = [[self.matrix[j][i] + n for i in range(self.rows)] for j in range(self.columns)]

    def __add__(self, other):
        new_matrix = Matrix(self.rows, self.columns)
        if self.columns == other.columns and self.rows == other.rows:
            mx = [[self.matrix[j][i] + other.matrix[j][i] for i in range(self.rows)] for j in range(self.columns)]
        new_matrix.double_array_to_matrix(mx)
        return new_matrix

    def __sub__(self, other):
        new_matrix = Matrix(self.rows, self.columns)
        if self.rows == other.rows and self.columns == other.columns:
            mx = [[self.matrix[j][i] - other.matrix[j][i] for i in range(self.rows)] for j in range(self.columns)]
        new_matrix.double_array_to_matrix(mx)
        return new_matrix

    def multiply(self, other):
        new_matrix = Matrix(self.rows, self.columns)
        if self.rows == other.rows and self.columns == other.columns:
            new_matrix.matrix = [[self.matrix[j][i] * other.matrix[j][i] for i in range(self.rows)] for j in
                                 range(self.columns)]
        return new_matrix

    def transpose(self):
        n = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                n.matrix[i][j] = self.matrix[j][i]
        return n

    @staticmethod
    def single_column_matrix_from_array(arr):
        new_matrix = Matrix(1, len(arr))
        for i in range(len(arr)):
            new_matrix.matrix[i][0] = arr[i]
        return new_matrix

    # sets matrix from an array
    def fromArray(self, arr):
        self.matrix = [[arr[j * self.columns + i] for j in range(self.rows)] for i in range(self.columns)]

    def toArray(self):
        arr = [self.matrix[i][j] for j in range(self.rows) for i in range(self.columns)]
        return arr

    def add_bias(self):
        n = Matrix(1, self.columns + 1)
        for i in range(self.columns):
            n.matrix[i][0] = self.matrix[i][0]
        n.matrix[self.columns][0] = 1
        return n

    def activate(self):
        new_matrix = Matrix(self.rows, self.columns)
        new_matrix.matrix = [[self.sigmoid(self.matrix[j][i]) for i in range(self.rows)] for j in range(self.columns)]
        return new_matrix

    # сам ни чё не понимаю, рабтает не трогаю
    def sigmoid_derivative(self):
        new_matrix = Matrix(self.rows, self.columns)
        new_matrix.matrix = [[(self.matrix[j][i] * (1 - self.matrix[j][i])) for i in range(self.rows)] for j in range(self.columns)]

    def remove_bottom_layer(self):
        n = Matrix(self.rows, self.columns - 1)
        n.matrix = [[self.matrix[j][i] for i in range(self.rows)] for j in range(self.columns - 1)]
        return n

    def mutate(self, mutation_rate):
        for i in range(self.columns):
            for j in range(self.rows):
                rand = random.uniform(0, 1)
                if rand < mutation_rate:
                    val = random.gauss()
                    self.matrix[i][j] += val / 5

                    if self.matrix[i][j] > 1:
                        self.matrix[i][j] = 1
                    elif self.matrix[i][j] < -1:
                        self.matrix[i][j] = -1

    def crossover(self, partner):
        child = Matrix(self.rows, self.columns)

        randC = random.randint(0, self.columns-1)
        randR = random.randint(0, self.rows-1)
        for i in range(self.columns):
            for j in range(self.rows):
                if i < randC or (i == randC and j <= randR):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]

        return child

    def clone(self):
        new_matrix = Matrix(self.rows, self.columns)
        new_matrix.matrix = [[self.matrix[i][j] for j in range(self.rows)] for i in range(self.columns)]
        return new_matrix


if __name__ == "__main__":
    mx = Matrix(3, 1)
    mx1 = Matrix(1, 3)
    print(mx, mx1, sep="\n\n", end='\n\n')
    mx.matrix = [[1, 2, 3], [4, 5, 6]]
    mx1.matrix = [[7, 8], [9, 10], [11, 12]]
    mx.matrix = [[1,2,3]]
    mx1.matrix = [[4],[5],[6]]
    print(mx, mx1, sep="\n\n", end='\n\n')

    print(mx1 * mx)
    #print(mx1 * mx)
