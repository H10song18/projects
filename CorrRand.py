import numpy as np
import matplotlib.pyplot as plt

mu_a, mu_b = 0.2, 0.3 # annual expected return for stock A and stock B
sig_a, sig_b = 0.25, 0.35 # annual expected volatility
s0_a, s0_b = 60, 55 # stock price at t0
T = 1 # simulate price evolution for the next year
delta_t = 0.001
steps = T / delta_t

rho = 0.2 # correlation between stock A and stock B
cor_matrix = np.array([[1.0, rho], [rho, 1.0]])
sd = np.diag([sig_a, sig_b])
cov_matrix = np.dot(sd, np.dot(cor_matrix, sd))

L = np.linalg.cholesky(cov_matrix) # Cholesky decomposition
plt.figure(figsize = (12, 6))
path_a = [s0_a]
path_b = [s0_b]
st_a, st_b = s0_a, s0_b


for i in range(int(steps)):
    V = L.dot(np.random.normal(0, 1, 2))
    st_a = st_a * np.exp((mu_a - 0.5*sig_a**2)*delta_t + sig_a*np.sqrt(delta_t)*V[0])
    st_b = st_b * np.exp((mu_b - 0.5*sig_b**2)*delta_t + sig_b*np.sqrt(delta_t)*V[1])
    path_a.append(st_a)
    path_b.append(st_b)


plt.plot(path_a, label = 'stock A', linewidth = 2)
plt.plot(path_b, label = 'stock B', linewidth = 2)
plt.legend()
plt.title('Correlated Stock Movement Using Monte Carlo Simulation')
plt.ylabel('stock price')
plt.xlabel('steps')
plt.show()