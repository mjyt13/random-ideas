import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Определение системы ОДУ
def system(t, P):
    P0, P1, P2, P3, P4 = P
    dP0dt = -2.2 * P0 + 0.5 * P1 + 1.7 * P3
    dP1dt = -2.5 * P1 + P0
    dP2dt = -2 * P2 + 1.2 * P0
    dP3dt = -1.7 * P3 + 2.5 * P4
    dP4dt = -2.5 * P4 + 2 * P1 + 2 * P2
    return [dP0dt, dP1dt, dP2dt, dP3dt, dP4dt]

# Начальные условия и временной интервал
P0 = [1.0, 0.0, 0.0, 0.0, 0.0]
t_span = (0, 10)  # От t=0 до t=10

# Решение системы
sol = solve_ivp(system, t_span, P0, method='RK45', dense_output=True)

# Визуализация
t = np.linspace(0, 10, 1000)
P = sol.sol(t)
plt.figure(figsize=(10, 6))
for i in range(5):
    plt.plot(t, P[i], label=f'$P_{i}(t)$')
plt.xlabel('$t$')
plt.ylabel('$P_i(t)$')
plt.legend()
plt.grid()
plt.title('Решение системы с использованием SciPy (solve_ivp)')
plt.show()