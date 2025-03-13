import numpy as np
import matplotlib.pyplot as plt

# Данные
n_values = [78, 101, 14, 26, 138, 65, 8, 15, 73, 86]
delta_t = 10
t_intervals = np.arange(0, 100, delta_t)
N = np.sum(n_values)

# Вероятность безотказной работы
N_values = []
N_1_2_values = []
P_t = []
f_t = []
lambda_t = []

N_values.append(N)
P_t.append(1)
f_t.append(n_values[0] / (N*delta_t))
for i in range(len(n_values) - 1):
    N_values.append(N - np.sum(n_values[0:i+1]) )
    P_t.append(N_values[i+1] / N)
    f_t.append(n_values[i+1] / (N*delta_t))
    N_1_2_values.append((N_values[-2] + N_values[-1]) / 2)
    lambda_t.append(n_values[i] / (N_1_2_values[i] * delta_t))
N_1_2_values.append(N_values[-1]/2)
lambda_t.append(n_values[-1] / (N_1_2_values[-1] * delta_t))

print(N_values)
print(N_1_2_values)
# Средняя наработка до отказа
for t,n in zip(t_intervals, n_values):
    print(t,n,t*n)
print(sum(t * n for t, n in zip(t_intervals, n_values)))
T_mean = sum(t * n for t, n in zip(t_intervals, n_values)) / N

# Дисперсия и среднее квадратическое отклонение
for t,n in zip(t_intervals, n_values):
    print(t,n,n * (t - T_mean)**2)
D_T = sum(n * (t - T_mean)**2 for t, n in zip(t_intervals, n_values)) / (N - 1)
sigma_T = np.sqrt(D_T)


# print(f'Вероятность безотказной работы: {P_t}')
print(f'Средняя наработка до отказа: {T_mean:.2f}')
print(f'Дисперсия времени безотказной работы: {D_T:.2f}')
print(f'Среднеквадратическое отклонение: {sigma_T:.2f}')
# print(f'Интенсивность отказов: {lambda_t}')
# print(f'Плотность распределения времени до отказа: {f_t}')


# Построение графиков в строку
plt.figure(figsize=(18, 5))

def add_labels(bars, values):
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.annotate(f'{value:.4f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=8)



# 1. Вероятность безотказной работы
plt.subplot(1, 3, 1)
bars = plt.bar(t_intervals, P_t, width=delta_t, align='edge', color='skyblue', edgecolor='black')
add_labels(bars, P_t)
plt.title('График вероятности отказов')
plt.xlabel('Интервал времени')
plt.ylabel('P(t)')

# 4. Интенсивность отказов
plt.subplot(1, 3, 2)
bars = plt.bar(t_intervals, lambda_t, width=delta_t, align='edge', color='red', edgecolor='black')
add_labels(bars, lambda_t)
plt.title('График интенсивности отказов')
plt.xlabel('Интервал времени')
plt.ylabel('λ(t)')

# 5. Плотность распределения времени до отказа
plt.subplot(1, 3, 3)
bars = plt.bar(t_intervals, f_t, width=delta_t, align='edge', color='purple', edgecolor='black')
add_labels(bars, f_t)
plt.title('График плотности распределения')
plt.xlabel('Интервал времени')
plt.ylabel('f(t)')

plt.tight_layout()
plt.show()
