from scipy.stats import uniform, norm, gamma
from scipy.optimize import brentq
from scipy.differentiate import derivative
import matplotlib.pyplot as plt
import numpy as np

def uniform_sf(x, a=100, b=5000):
    return uniform.sf(x, loc=a, scale=b - a)

def norm_sf(x, mu=500, sigma=10000**(1/2)):
    return norm.sf(x, loc=mu, scale=sigma)

def gamma_sf(x, k=8, teta=65):
    return gamma.sf(x,a=k,scale=teta)


def combined_sf(x):
    S_uniform = uniform_sf(x)
    S_norm = norm_sf(x)
    S_gamma = gamma_sf(x)
    return S_uniform * S_norm * S_gamma

def combined_pdf(x, dx=1e-5):
    # Численная производная от CDF = 1 - SF
    return derivative(lambda t: 1 - combined_sf(t),
        x)

def hazard_rate(x):
    pdf = combined_pdf(x)["df"]
    sf = combined_sf(x)
    return np.where(sf > 1e-10, pdf / sf, np.inf)

def gamma_work(p_gamma, t_min=1, t_max=5000):
    target = p_gamma / 100
    func = lambda t: (1 - combined_sf(t)) - target
    try:
        return brentq(func, t_min, t_max)
    except ValueError:
        return np.nan

def plot_graphs():
    t_values = np.linspace(0, 6000, 100)
    f_values = [combined_pdf(t)["df"] for t in t_values]
    P_values = [combined_sf(t) for t in t_values]
    lambda_values = [hazard_rate(t) for t in t_values]
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
