import numpy as np
import matplotlib
from math import exp,pow,factorial
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Параметры гамма-распределения
k, teta = 8, 65

# метод прямоугольников
def gamma_function(k, steps=1000):
    def integrand(t):
        return t ** (k - 1) * exp(-t)
    dt = 10.0 / steps  # Интегрируем от 0 до 10 (условная бесконечность)
    integral = 0.0
    for i in range(steps):
        t = i * dt
        integral += integrand(t) * dt
    # print(f"gangsta {k}")
    return integral

# 5. Плотность распределения вероятности безотказной работы
def density_probability(t):
    if t < 0: return 0
    else: return (pow(t,k-1)*exp(-t/teta))/(pow(teta,k)*gamma_function(k))

def density_moment_1(t):
    if t < 0: return 0
    else: return (pow(t,k)*exp(-t/teta))/(pow(teta,k)*gamma_function(k))

def density_moment_2(t):
    if t < 0: return 0
    else: return (pow(t,k+1)*exp(-t/teta))/(pow(teta,k)*gamma_function(k))

# 1. Функция надёжности: вероятность безотказной работы
def reliability_function(t,dt=1e-2):

    integral = 0
    for i in range(0,k+1):
        integral += (t**i)/(teta**i*factorial(i))
    # steps = int(t/dt)
    # integral = 0.0
    # for i in range(steps):
    #     integral += density_probability(i*dt) * dt
    integral *= exp(-t/teta)

    return integral

def rejection_function(t):
    return 1-reliability_function(t)

# 2. Средняя наработка до отказа (матожидание)
def mean_time_until_reject(b=1200,dt=1e-2):
    print(f"mat. ozhidanie")
    steps = int(b/dt)
    integral = 0.0
    for i in range(steps):
        integral += density_moment_1(i * dt) * dt
        if i%100==0: print(i)
    return integral

# 3. Дисперсия времени безотказной работы
def quad_varience(b=1200,dt=1e-2):
    print(f"dispersia")
    steps = int(b/dt)
    integral = 0.0
    for i in range(steps):
        integral += density_moment_2(i * dt) * dt
        if i % 100 == 0: print(i)
    return integral

# 4. Интенсивность отказов
def hazard_rate(t):
    sf = reliability_function(t)
    pdf = density_probability(t)
    print(pdf/sf)
    return np.where(pdf == 0 and sf == 0,np.inf,pdf/sf)

# 6. Гамма-процентная наработка
def gamma_work(percent,a=0,b=1300,stop=1e-6,iters=100):
    gamma = percent/100
    fa = rejection_function(a) - gamma
    fb = rejection_function(b) - gamma

    for _ in range(iters):
        c = (a + b) / 2
        fc = rejection_function(c) - gamma

        if abs(fc) < stop:
            return c

        if fc * fa < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return (a + b) / 2

# mean_time = mean_time_until_reject()
# variance = quad_varience()-mean_time**2 # 3. Дисперсия времени безотказной работы
# print(f'Средняя наработка до отказа: {mean_time:.2f}')
# std_dev = np.sqrt(variance)  # 3. Среднеквадратическое отклонение
# print(f'Дисперсия: {variance:.2f}, СКО: {std_dev:.2f}')

# Подготовка данных для графиков:
t_values = np.linspace(0, 1300, 1000)
reliability_values = [reliability_function(t) for t in t_values]
density_values = [density_probability(t) for t in t_values]
hazard_values = [hazard_rate(t) for t in t_values]

# 6. Гамма-процентная наработка: определяем времена для γ = 0, 10, 20, …, 100%
gamma_values = np.arange(0, 101, 10)
gamma_life = [gamma_work(g) for g in gamma_values]

# Создаем фигуру с 6 субграфиками (3 строки x 2 столбца)
fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# Вывод расчетных значений в консоль:
# print(f'Дисперсия: {variance:.2f}, СКО: {std_dev:.2f}')

# График 1: Функция надёжности
axs[0, 0].plot(t_values, reliability_values, color='green')
axs[0, 0].set_title('Функция надежности')
axs[0, 0].set_xlabel('Время')
axs[0, 0].set_ylabel('Вероятность безотказной работы')

# График 4: Интенсивность отказов
axs[0, 1].plot(t_values, hazard_values, color='red')
axs[0, 1].set_title('Интенсивность отказов')
axs[0, 1].set_xlabel('Время')
axs[0, 1].set_ylabel('λ (отказов/ед. времени)')

# График 5: Плотность распределения времени до отказа (PDF)
axs[1, 0].plot(t_values, density_values, color='blue')
axs[1, 0].set_title('Плотность распределения (PDF)')
axs[1, 0].set_xlabel('Время')
axs[1, 0].set_ylabel('Плотность вероятности')

# График 6: Гамма-процентная наработка до отказа
axs[1, 1].plot(gamma_values, gamma_life, marker='o', linestyle='-', color='brown')
axs[1, 1].set_title('Гамма-процентная наработка до отказа')
axs[1, 1].set_xlabel('γ (%)')
axs[1, 1].set_ylabel('Время')

plt.tight_layout()
plt.show()


