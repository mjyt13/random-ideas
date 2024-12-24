
M = 1e4

simplex_table = [
    [-20*M,-3*M-3,-4*M+2,0,0,M,0],
    [11,2,1,1,0,0,0],
    [10,-3,2,0,1,0,0],
    [20,3,4,0,0,-1,1]
]

solution = [0,0,0,0,0,0]
indexes = []

def find_leading_column(matrix):
    temp_matrix = matrix[0].copy()
    temp_matrix.pop(0)
    lead_column = temp_matrix.index(min(temp_matrix))
    return lead_column + 1

def find_leading_row(matrix):
    lead_column = find_leading_column(matrix)
    quotients = []
    for i in range(1, len(matrix)):
        if matrix[i][lead_column] > 0:
            quotients.append(matrix[i][0]/matrix[i][lead_column])
        else:
            quotients.append(1e8)
    lead_row = quotients.index(min(quotients))
    return lead_row + 1

def write_new_table(matrix):
    lead_row = find_leading_row(matrix)
    lead_column = find_leading_column(matrix)
    new_matrix = []
    matrix_row = []
    # YOSHA!
    lead_element = matrix[lead_row][lead_column]
    for i in range(len(matrix)):
        if i != lead_row:
            for j in range(len(matrix[0])):
                if j != lead_column:
                    matrix_row.append(
                        matrix[i][j] - (matrix[i][lead_column] * matrix[lead_row][j]) / lead_element
                    )
                else:
                    matrix_row.append(0)
        else:
            for j in range(len(matrix[0])):
                matrix_row.append(matrix[i][j] / lead_element)
        # print(matrix_row)
        new_matrix.append(matrix_row.copy())
        matrix_row.clear()
    return new_matrix

# чисто проверка на неотрицательность элементов первой строки
M = 1e4

simplex_table = [
    [-20*M,-3*M-3,-4*M+2,0,0,M,0],
    [11,2,1,1,0,0,0],
    [10,-3,2,0,1,0,0],
    [20,3,4,0,0,-1,1]
]

solution = [0,0,0,0,0,0]
indexes = []

def find_leading_column(matrix):
    temp_matrix = matrix[0].copy()
    temp_matrix.pop(0)
    lead_column = temp_matrix.index(min(temp_matrix))
    return lead_column + 1

def find_leading_row(matrix):
    lead_column = find_leading_column(matrix)
    quotients = []
    for i in range(1, len(matrix)):
        if matrix[i][lead_column] > 0:
            quotients.append(matrix[i][0]/matrix[i][lead_column])
        else:
            quotients.append(1e8)
    lead_row = quotients.index(min(quotients))
    return lead_row + 1

def write_new_table(matrix):
    lead_row = find_leading_row(matrix)
    lead_column = find_leading_column(matrix)
    new_matrix = []
    matrix_row = []
    # YOSHA!
    lead_element = matrix[lead_row][lead_column]
    for i in range(len(matrix)):
        if i != lead_row:
            for j in range(len(matrix[0])):
                if j != lead_column:
                    matrix_row.append(
                        matrix[i][j] - (matrix[i][lead_column] * matrix[lead_row][j]) / lead_element
                    )
                else:
                    matrix_row.append(0)
        else:
            for j in range(len(matrix[0])):
                matrix_row.append(matrix[i][j] / lead_element)
        # print(matrix_row)
        new_matrix.append(matrix_row.copy())
        matrix_row.clear()
    return new_matrix

# чисто проверка на неотрицательность элементов первой строки
def simplex_done(matrix):
    for i in range(len(matrix[0])):
        if matrix[0][i] < 0:
            return False
    return True

def simplex_unsolving(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                return False
    return True

while not(simplex_done(simplex_table)):
    if simplex_unsolving(simplex_table):
        print('решений у задачи нет')
        break
    print(simplex_table)
    indexes.append((find_leading_row(simplex_table), find_leading_column(simplex_table)))
    simplex_table = write_new_table(simplex_table)


for row in simplex_table:
    for column in row:
        print(f"{round(column,4)}", end="\t")
    print()

for cortez in indexes:
    solution[cortez[1]-1] = simplex_table[cortez[0]][0]

print()

print("Решение найдено")
for i in range(len(solution)):
    print(f"x{i} = {round(solution[i],2)}",end="\t")
print(f"\nf={simplex_table[0][0]}")
