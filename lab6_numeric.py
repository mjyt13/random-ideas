import numpy as np
import matplotlib.pyplot as plt


# Определение системы ОДУ
def system(t, P):
    P0, P1, P2, P3, P4 = P
    dP0dt = -2.2 * P0 + 0.5 * P1 + 1.7 * P3
    dP1dt = -2.5 * P1 + P0
    dP2dt = -2 * P2 + 1.2 * P0
    dP3dt = -1.7 * P3 + 2.5 * P4
    dP4dt = -2.5 * P4 + 2 * P1 + 2 * P2
    return np.array([dP0dt, dP1dt, dP2dt, dP3dt, dP4dt])


# Начальные условия
P0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])  # P0(0)=1, P1(0)=0, ..., P4(0)=0
t0, t_end = 0, 10  # Временной интервал
h = 0.3  # Шаг


# Метод Рунге-Кутты 4-го порядка
def rk4(f, y0, t0, t_end, h):
    t = np.arange(t0, t_end + h, h)
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(1, len(t)):
        k1 = h * f(t[i - 1], y[i - 1])
        k2 = h * f(t[i - 1] + h / 2, y[i - 1] + k1 / 2)
        k3 = h * f(t[i - 1] + h / 2, y[i - 1] + k2 / 2)
        k4 = h * f(t[i - 1] + h, y[i - 1] + k3)
        y[i] = y[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return t, y


# Решение
t, P = rk4(system, P0, t0, t_end, h)

# Визуализация
plt.figure(figsize=(10, 6))
for i in range(5):
    plt.plot(t, P[:, i], label=f'$P_{i}(t)$')
plt.xlabel('$t$')
plt.ylabel('$P_i(t)$')
plt.legend()
plt.grid()
plt.title('Решение системы методом Рунге-Кутты 4-го порядка')
plt.show()
