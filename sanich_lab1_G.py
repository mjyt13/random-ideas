from scipy.stats import gamma
import numpy as np
import matplotlib.pyplot as plt

k = 8
teta = 65

dist = gamma(a=8,scale=teta)  # для гамма-распределения

# 1. Вероятность безотказной работы (SF = 1 - CDF)
def u_sf(x):
    sf = dist.sf(x)  # P(X > x)
    return sf

# 2. Математическое ожидание
mean = dist.mean()  # E[X]

# 3. Дисперсия и СКО
var = dist.var()    # Var[X]
std = dist.std()    # sqrt(Var[X])

# 4. Интенсивность отказов (Hazard Rate)
def u_hazard_rate(x):
    hazard = dist.pdf(x) / dist.sf(x)  # λ(x) = f(x) / (1 - F(x))
    return hazard

# 5. Плотность распределения (PDF)
def u_pdf(x):
    pdf = dist.pdf(x)   # f(x)
    return pdf

# 6. Гамма-процентная наработка (ppf = обратная CDF)
def gamma_work(p_gamma):
    target = p_gamma / 100
    try:
        gamma_time = dist.ppf(target)
        return gamma_time
    except ValueError:
        return np.nan

def plot_graphs():
    t_values = np.linspace(0, 2000, 1000)
    f_values = [u_pdf(t) for t in t_values]
    P_values = [u_sf(t) for t in t_values]
    lambda_values = [u_hazard_rate(t) for t in t_values]
    gamma_labels = list(range(0, 110, 10))
    gamma_values = [gamma_work(g) for g in gamma_labels]
    gamma_values[0] = 0
    print(gamma_values)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # График 1: Плотность распределения f(t)
    axs[0, 0].plot(t_values, f_values, label="f(t)", color="tab:blue")
    axs[0, 0].set_xlabel("Время t")
    axs[0, 0].set_ylabel("f(t)")
    axs[0, 0].set_title("Плотность распределения f(t)")
    axs[0, 0].legend()
    axs[0, 0].grid()

    # График 2: Вероятность безотказной работы P(t)
    axs[0, 1].plot(t_values, P_values, label="P(t)", color="tab:green")
    axs[0, 1].set_xlabel("Время t")
    axs[0, 1].set_ylabel("P(t)")
    axs[0, 1].set_title("Вероятность безотказной работы P(t)")
    axs[0, 1].legend()
    axs[0, 1].grid()

    # График 3: Гамма-процентная наработка T_gamma
    axs[1, 0].plot(gamma_labels, gamma_values[::-1], "ko-", label="gamma")
    axs[1, 0].set_xlabel("γ, %")
    axs[1, 0].set_ylabel("Время gamma")
    axs[1, 0].set_title("Гамма-процентная наработка")
    axs[1, 0].legend()
    axs[1, 0].grid()

    # График 4: Интенсивность отказов λ(t)
    axs[1, 1].plot(t_values, lambda_values, label="λ(t)", color="tab:red")
    axs[1, 1].set_xlabel("Время t")
    axs[1, 1].set_ylabel("λ(t)")
    axs[1, 1].set_title("Интенсивность отказов λ(t)")
    axs[1, 1].legend()
    axs[1, 1].grid()

    plt.tight_layout()
    plt.show()


plot_graphs()
