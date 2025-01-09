def f(x):
    return 2 * x[0]**2 + x[1]**2 + x[0]*x[1] + x[0] + x[1]


def grad_f(x):
    x1 = 4 * x[0] + x[1] + 1
    x2 = 2 * x[1] + x[0] + 1
    return [x1,x2]


# start point
x0 = [0,0]
# accelerating parameter
lamb0 = 1
epsilon = 1e-6

def hook_jiws(x0, lambd, epsilon):
    xk = x0.copy()
    lamb_0 = float(lambd)
    lamb = lamb_0
    iterations = 0
    alpha = 1
    # fails
    p = 0
    while lamb >= epsilon:
        iterations += 1
        elems = [xk]
        # пройти по координатам точки
        for i in range(len(xk)):
            temp_elems = []
            # создать по 3 точки для каждой из существующих на этапе работы с конкретной координатой
            for elem in elems:
                x1 = elem.copy()
                # это для xi - λ
                x1[i] -= lamb
                x2 = elem.copy()
                x3 = elem.copy()
                # это для xi + λ
                x3[i] += lamb
                temp_elems.append(x1)
                temp_elems.append(x2)
                temp_elems.append(x3)
            # и закинуть новые точки к существующим
            elems = elems + temp_elems
            temp_elems.clear()
        # удалить все повторяющиеся точки
        for elem in elems:
            if elems.count(elem)!=1:
                elems.remove(elem)
        # удалить из списка точек начальную для определения направления
        elems.remove(xk)
        # найти минимумы функции
        func_values = []
        for elem in elems:
            func_values.append(f(elem))
        min_f = min(func_values)
        min_x = elems[func_values.index(min_f)]
        f_x = f(xk)
        # и сравнить значений
        if round(min_f,4) >= round(f_x,4):
            p += 1
            # не получилось, надо изменить "шаг"
            # lamb = lamb - (lamb_0 / m.exp(p))
            lamb /= 2.0
        else:
            xk = xk
            for i in range(len(min_x)):
                # получилось, по формуле x0 переходит в следующую итерацию
                min_x[i] -= xk[i]
                min_x[i] *= alpha
                xk[i] = min_x[i] + xk[i]
            p = 0
        # очистить списки точек, все операции в итерации завершены
        func_values.clear()
        elems.clear()

    return xk, f(xk), iterations


def gradient_const(x0, lamb, epsilon):
    # точки
    xk = x0.copy()
    xk_1 = xk.copy()
    iterations = 1
    # найти градиент в точке
    g = grad_f(xk)
    # пройти в направлении, противоположном градиенту
    for i in range(len(xk)):
        xk_1[i] = xk[i] - g[i] * lamb

    while abs(f(xk_1)-f(xk)) >= epsilon:
        iterations += 1
        xk = xk_1.copy()
        g = grad_f(xk)
        for i in range(len(xk)):
            xk_1[i] = xk[i] - g[i] * lamb
        if f(xk_1) >= f(xk):
            lamb /= 2
    return xk_1, f(xk_1), iterations

print(f"т. мин = {hook_jiws(x0, lamb0, epsilon)[0]} мин. знач. = {hook_jiws(x0, lamb0, epsilon)[1]} "
      f"кол-во итераций {hook_jiws(x0, lamb0, epsilon)[2]}")

print(f"т. мин = {gradient_const(x0,lamb0,epsilon)[0]} мин. знач. = {gradient_const(x0,lamb0,epsilon)[1]} "
      f"кол-во итераций {gradient_const(x0,lamb0,epsilon)[2]}")
