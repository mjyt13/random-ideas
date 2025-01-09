from matplotlib import pyplot as plt
import math
from sympy import *
import random

x = symbols('x')


# изначальная функция, минимум которой ищется в этой программе
def f(x):
     return x**5 - (5 * x**3) + (10 * x**2) - 5*x


def f_minus(x):
    return -x ** 5 + (5 * x ** 3) - (10 * x ** 2) + 5 * x

# производная функции
def df(x):
    return 5* x**4 - 15 * x**2 + 20 * x - 5


def df_minus(x):
    return - 5 * x**4 + 15 * x**2 - 20*x + 5


# вторая производная
def d2f(x):
    return 20 * x**3 - 30 * x + 20


def d2f_minus(x):
    return -20 * x**3 + 30 * x - 20

# отрисовка графика
def graphic(a,b):
    plt.grid(true)
    i = a
    args = []
    fargs = []
    while i<=b:
        args.append(i)
        fargs.append(f(i))
        i+=0.001
    plt.plot(args,fargs)
    plt.show()
    pass


# отрисовка графика функции, домноженной на (-1)
def df_graphic(a,b):
    plt.grid(true)
    i = a
    args = []
    fargs = []
    while i <= b:
        args.append(i)
        fargs.append(f_minus(i))
        i += 0.001
    plt.plot(args, fargs)
    plt.show()
    pass


# точки отрезка и точность
a = 0
b = 3
epsilon = 1e-1


# метод золотого сечения
def gold_glowing(a, b, epsilon):
    # обозначаются параметры
    ak = a
    bk = b
    eps = epsilon
    # затем точки
    x1 = ak + ((3 - math.sqrt(5)) / 2) * (bk - ak)
    x2 = ak + ((math.sqrt(5) - 1) / 2) * (bk - ak)
    # и задаётся количество итераций
    iterations = 0
    while abs(bk - ak) >= eps:
        # новая итерация
        iterations += 1
        # print(f"b - a = {bk - ak}")
        # Найти разницу между двумя переменными
        # В следующей итерации она будет определять расстояние от начала отрезка до точки золотого сечения
        c = x2 - x1
        if f(x1) >= f(x2):
            # здесь точка деления находится слева от середины
            ak = x1
            bk = bk
            x1 = x2
            x2 = bk - c
        else:
            # здесь точка деления находится справа
            ak = ak
            bk = x2
            x2 = x1
            x1 = ak + c
    """после завершения поиска необходимого отрезка выбирается точка
     посередине найденного отрезка, и от неё находится значение функции"""
    xmin = (ak + bk) / 2
    ymin = f(xmin)
    return xmin, ymin, iterations


def gold_glowing_minus(a, b, epsilon):
    ak = a
    bk = b
    eps = epsilon
    x1 = ak + ((3 - math.sqrt(5)) / 2) * (bk - ak)
    x2 = ak + ((math.sqrt(5) - 1) / 2) * (bk - ak)
    iterations = 0
    while abs(bk - ak) >= eps:
        iterations += 1
        c = x2 - x1
        if f_minus(x1) >= f_minus(x2):
            # здесь точка деления находится слева от середины
            ak = x1
            bk = bk
            x1 = x2
            x2 = bk - c
        else:
            ak = ak
            bk = x2
            x2 = x1
            x1 = ak + c
    """после завершения поиска необходимого отрезка выбирается точка
     посередине найденного отрезка, и от неё находится значение функции"""
    xmin = (ak + bk) / 2
    ymin = f(xmin)
    return xmin, ymin, iterations


def dixotomy_minus(a, b, epsilon, delta):
    ak = a
    bk = b
    eps = epsilon
    delt = delta
    x1 = (ak + bk - delt)/2
    x2 = (ak + bk + delt)/2
    iterations = 0
    while abs(bk - ak) >= eps:
        iterations += 1
        if f_minus(x1) >= f_minus(x2):
            ak = x1
            bk = bk
            x1 = (ak + bk - delt)/2
            x2 = (ak + bk + delt) / 2
        else:
            ak = ak
            bk = x2
            x2 = (ak + bk + delt) / 2
            x1 = (ak + bk - delt)/2

    xmin = (ak + bk) / 2
    ymin = f(xmin)
    return xmin, ymin, iterations


# функция поиска пересечения двух касательных (точки на входе - переменные,
# от которых находится производная функции)
def intersection(xl, xr):
    xm = (df(xl) * xl - df(xr) * xr + f(xr) - f(xl)) / (df(xl) - df(xr))
    return xm


def intersection_minus(xl,xr):
    xm = (df_minus(xl) * xl - df_minus(xr) * xr + f_minus(xr) - f_minus(xl)) / (df_minus(xl) - df_minus(xr))
    return xm

# метод касательных
def tangles(a, b, epsilon):
    # найти точку пересечения касательных к функции в концах заданного отрезка
    xm = intersection(a, b)
    xm_1 = b
    # завести количество итераций для метода
    iterations = 0
    # в сущности необходима близость модуля производной искомой точки к нулю
    # из-за использования импортируемых функций (numpy diff) точность ниже 10^(-4) вызывает ошибку
    while abs(f(xm)-f(xm_1)-df(xm_1)*(xm-xm_1))>=epsilon:
        # print(xm)
        iterations += 1
        # Найти правые и левые точки пересечения касательных к ф. в концах отрезка с оной в ранее найденной т.
        xl = intersection(a, xm)
        xr = intersection(xm, b)
        # если производная в точке оказывается больше нуля, функция справа от этого значения только возрастает
        # стало быть, необходимо уменьшить отрезок поиска, выбросив все значения после точки xr
        if df(xm) > 0:
            xr = xm
        # если же производная оказывается меньше нуля, функция слева от точки только убывает
        # тогда необходимо отбросить диапазон до xl
        elif df(xm) < 0:
            xl = xm
        # после уменьшения отрезка находится новая точка пересечения касательных,
        # которую можно проверить на близость к минимуму
        a = xl
        b = xr
        xm_1 = xm
        xm = intersection(xl, xr)
    return xm, f(xm), iterations


def tangles_minus(a, b, epsilon):
    xm = intersection(a, b)
    xm_1 = xm * 100000
    iterations = 0
    delta1 = abs(df_minus(xm))
    delta2 = abs(f_minus(xm) - f_minus(xm_1) - df_minus(xm_1) * (xm - xm_1))
    while delta1 >= epsilon and delta2 >= epsilon:
        iterations += 1
        xl = intersection(a, xm)
        xr = intersection(xm, b)
        if df_minus(xm) > 0:
            xr = xm
        elif df_minus(xm) < 0:
            xl = xm
        a = xl
        b = xr
        delta1 = abs(df_minus(xm))
        delta2 = abs(f_minus(xm)-f_minus(xm_1)-df_minus(xm_1)*(xm-xm_1))
        xm_1 = xm
        xm = intersection(a, b)
    return xm, f(xm), iterations

# метод Ньютона
def newton(a, epsilon):
    # обозначить точки для итерации (текущая и следующая)
    xk = a
    xk_1 = a+0.1
    iterations = 0
    while abs(xk - xk_1) >= epsilon or abs(f(xk) - f(xk_1)) >= epsilon:
        # после перейти к вычислению следующего значения с сохранением предыдущего
        iterations += 1
        if iterations > 1:
            xk = xk_1
        df1 = df(xk)
        d2f1 = d2f(xk)
        xk_1 = xk - (df1 / d2f1)
    return xk_1, f(xk_1), iterations


def newton_minus(a,b,epsilon):
    xk = a
    xk_1 = a + 0.1
    iterations = 0
    while abs(xk - xk_1) >= epsilon or abs(f_minus(xk) - f_minus(xk_1)) >= epsilon:
        # после перейти к вычислению следующего значения с сохранением предыдущего
        iterations += 1
        if iterations > 1:
            xk = xk_1
        df1 = df_minus(xk)
        d2f1 = d2f_minus(xk)
        xk_1 = xk - (df1 / d2f1)
    return xk_1, f(xk_1), iterations

def vipuklost(a,b):
    i = a
    j = a
    alfa = random.random()
    while i<=b:
        while j<=b:
            if f(alfa * i + (1-alfa)*j) <= alfa * f(i) + (1-alfa) * f(j):
                return False
            j += 1e-4
        i+=1e-4
        j = a
    return True

def main():
    # print("метод нулевого порядка в любом случае найдёт минимум")
    # print(gold_glowing(a,b,epsilon))
    if not vipuklost(a,b):
        # print("Метод первого и второго порядка не найдут минимум функции")
        # print("Тогда можно найти максимум (экстремум) функции")
        # print(gold_glowing_minus(a,b,epsilon))
        # print(tangles_minus(a,b,epsilon))
        print(newton_minus(a,b,epsilon))
    else:
        # print(tangles(a,b,epsilon))
        print(newton(a,b,epsilon))

    # graphic(a,b)
    # df_graphic(a,b)
main()