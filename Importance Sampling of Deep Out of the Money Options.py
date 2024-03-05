import numpy as np
import scipy as sc
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def blackScholes(r, S, K, T, sigma, opt_type="c"):
    "Calculate BS price of call/put"
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if opt_type == "c":
            price = S*sc.stats.norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*sc.stats.norm.cdf(d2, 0, 1)
        elif opt_type == "p":
            price = K*np.exp(-r*T)*sc.stats.norm.cdf(-d2, 0, 1) - S*sc.stats.norm.cdf(-d1, 0, 1)
        return price
    except:
        print("Please confirm option type, either 'c' for Call or 'p' for Put!")


# Initialise parameters
S0 = 100.0     # initial stock price
K = 170.0      # strike price
T = 1.0        # time to maturity in years
r = 0.06       # annual risk-free rate
vol = 0.20     # volatility (%)

dt = T
nudt = (r - 0.5*vol**2)*dt
nudt2 = (np.log(K/S0)-0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)


BS = blackScholes(r, S0, K, T, vol)
print("Black Scholes Price: ", round(BS,4))


M = 1000000
Z = np.random.normal(0,1, M)

# Indicator function, count number of sampled variables above 25
ZT = np.where(Z>25,1,0)
X = np.mean( ZT )

# Calculate standard error and 95% Condifence intervals
sigma = np.std(ZT)
SE = sigma/np.sqrt(M)
CIs = [X-SE*1.96,X+SE*1.96]

print('95% Confidence Levels for 25 St Dev. Returns are [{:0.3e}, {:0.3e}]'.format(CIs[0], CIs[1]))


M = 1000
mu=25

Z = np.random.normal(mu,1, M)

p = sc.stats.norm(0, 1)
q = sc.stats.norm(mu, 1)

ZT = np.where(Z>25,1,0)*p.pdf(Z)/q.pdf(Z)


X = np.mean( ZT )
sigma = np.std(ZT)
SE = sigma/np.sqrt(M)
CIs = [X-SE*1.96,X+SE*1.96]

print('95% Confidence Levels for 25 St Dev. Returns are [{:0.3e}, {:0.3e}]'.format(CIs[0], CIs[1]))


M = 100
N = 52

#precompute constants
dt = T/N
nudt = (r - 0.5*vol**2)*dt
nudt2 = (np.log(K/S0)-0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)
lnS = np.log(S0)

# Monte Carlo Method
Z = np.random.normal(0,1,size=(N, M))

delta_lnSt = nudt + volsdt*Z
lnSt = lnS + np.cumsum(delta_lnSt, axis=0)
lnSt = np.concatenate( (np.full(shape=(1, M), fill_value=lnS), lnSt ) )

delta_lnSt2 = nudt2 + volsdt*Z
lnSt2 = lnS + np.cumsum(delta_lnSt2, axis=0)
lnSt2 = np.concatenate( (np.full(shape=(1, M), fill_value=lnS), lnSt2 ) )

ST = np.exp(lnSt)
ST2 = np.exp(lnSt2)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,6))
fig.suptitle('Importance Sampling: Change of Measure - Girsanovs Lemma')
ax1.plot(ST)
ax1.plot([0,N],[K,K],'k--',linewidth=3)

ax2.plot(ST2)
ax2.plot([0,N],[K,K],'k--',linewidth=3)

plt.show()



print("Black Scholes Price: ", round(BS,4))


# Initialise parameters
S0 = 100.0     # initial stock price
K = 170.0      # strike price
T = 1.0        # time to maturity in years
r = 0.06       # annual risk-free rate
vol = 0.20     # volatility (%)

dt = T
nudt = (r - 0.5*vol**2)*dt
nudt2 = (np.log(K/S0)-0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)


p = sc.stats.norm(nudt,volsdt)
q = lambda mu: sc.stats.norm(mu, volsdt)
z_T = lambda x, mu, sig: mu + sig*x
f_0 = lambda z: np.exp(-r*T)*np.maximum(0, S0*np.exp(z)-K)

M = 1000000
def arg_min(x):
    x_T = np.random.normal(0, 1, M)
    z = z_T(x_T,nudt,volsdt)
    return np.mean( f_0(z)**2 * p.pdf(z)/q(x).pdf(z) )

mu_star = sc.optimize.fmin(lambda x: arg_min(x), nudt2, disp=True)
mu_star

C0_is, SE_is = [], []
for M in np.arange(100,1000+100,100):
    mu = mu_star[0]
    x = np.random.randn(M)
    z = z_T(x,mu,volsdt)
    CT = f_0(z) * p.pdf(z)/q(mu).pdf(z)
    C0 = np.mean( CT )

    sigma = np.sqrt( np.sum( (CT - C0)**2) / (M-1) )
    SE = sigma/np.sqrt(M)

    C0_is.append(C0)
    SE_is.append(SE)

C0_is = np.array(C0_is)
SE_is = np.array(SE_is)

print("Call value is ${0} with SE +/- {1}".format(np.round(C0_is,3),np.round(SE_is,3)))


C0_wo, SE_wo = [], []
for M in np.arange(100,1000+100,100):
    x = np.random.randn(M)
    z = z_T(x, nudt, volsdt)
    CT = f_0(z)
    C0 = np.mean( CT )

    sigma = np.sqrt( np.sum( (CT - C0)**2) / (M-1) )
    SE = sigma/np.sqrt(M)
    C0_wo.append(C0)
    SE_wo.append(SE)

C0_wo = np.array(C0_wo)
SE_wo = np.array(SE_wo)

print("Call value is ${0} with SE +/- {1}".format(np.round(C0_wo,3),np.round(SE_wo,3)))



SE_Ratio = SE_wo/SE_is

print("Standard Error Reduction Factor {0}".format(np.round(SE_Ratio,3)))


import pandas as pd

M = np.arange(100,1000+100,100)
prices = pd.DataFrame(np.array([M, C0_wo.round(3), C0_is.round(3), SE_wo.round(3), SE_is.round(3), SE_Ratio.round(1)]).T,
                      columns=['Simulations','Price_wo', 'Price_is','SE_wo', 'SE_is', 'Reduction'])

print("Black Scholes Price: ", round(BS,4))
prices




