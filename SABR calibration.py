# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

     

def SABR_market_vol(K,f,t_exp,alpha,beta,nu,rho):
    output = np.zeros(len(K))
    
    for i in range(0,len(K)):
        if K[i] == f: #ATM equation in Managing smile risk
            part_1 = (1.0 - beta)**2.0 * alpha**2.0 / (24.0 * f**(2.0 - 2.0*beta))
            part_2 = rho * beta * alpha * nu / (4.0*f**(1.0 - beta))
            part_3 = (2.0 - 3.0 * rho**2) * nu**2.0 / 24.0
            
            output[i] = (alpha/f**(1 - beta))*(1 + (part_1 + part_2 + part_3)*t_exp )
        
        else:
            logfK = np.log(f/K[i])
            fkbpow = (f*K[i])**((1.0 - beta)/2.0)
            z = nu*fkbpow*logfK/alpha
            xz = np.log((np.sqrt(1.0 - 2.0*rho*z + z**2.0 ) + z - rho)/(1.0-rho))
            
            part_1 = ((1.0-beta)**2.0)*(alpha**2.0)/(24.0*fkbpow**2.0)
            part_2 = (rho*beta*nu*alpha)/(4.0*fkbpow)
            part_3 = (2.0-3.0*rho**2)*nu**2.0/24.0
            part_4 = ((1.0-beta)**2)*(logfK**2)/24.0
            part_5 = ((1.0-beta)**4)*(logfK**4)/1920.0
            
            output[i] = (alpha*z*(1 + (part_1 + part_2 + part_3)*t_exp ))/(fkbpow*xz*(1 + part_4 + part_5 ))
            
    return output

def atm_sigma_to_alpha(f,t_exp,sigma_atm,beta,nu,rho):

    p_3 = -sigma_atm
    p_2 =  (1 + ((2-3*rho**2) * nu**2 * t_exp) / 24) / f**(1.-beta)
    p_1 = rho * beta * nu * t_exp / (4 * f**(2-2*beta))
    p_0 = (1-beta)**2 * t_exp / (24 * f**(3-3*beta))
    coeffs = [p_0, p_1, p_2, p_3]
    
    r = np.roots(coeffs)    #find the roots of the cubic equation
    
    return r[(r.imag==0) & (r.real>=0)].real.min() 

def SABR_calibration(f, t_exp, sigma_atm, beta, strikes, vols, guess):

    def func_to_optimize(K, nu, rho):
        alpha = atm_sigma_to_alpha(f, t_exp, sigma_atm, beta, nu, rho)
        return  SABR_market_vol(K, f, t_exp, alpha, beta, nu, rho)
     
    popt, pcov = curve_fit(func_to_optimize, strikes, vols, p0 = (guess[1],guess[2]), maxfev=10000)
      
    nu = popt[0]
    rho = popt[1]
    alpha = atm_sigma_to_alpha(f,t_exp,sigma_atm,beta,nu,rho)
    
    return [alpha, nu, rho]

def SABR_calibration2(f, t_exp, sigma_atm, beta, strikes, vols, guess):

    def func_to_optimize(K, alpha, nu, rho):
        return  SABR_market_vol(K, f, t_exp, alpha, beta, nu, rho)
     
    popt, pcov = curve_fit(func_to_optimize, strikes, vols, p0=(guess[0],guess[1],guess[2]), maxfev=10000)
    
    alpha = popt[0]
    nu = popt[1]
    rho = popt[2]
    
    return [alpha, nu, rho]

    
if __name__ == "__main__":
 
    beta = 0.5
    #The current forward price
    f =  0.028436364   
    #The time to the expiry of the option
    t_exp = 5
    #The tenor of the option
    tenor = 2
    #A list of market volatilities at strikes corropsponding to strikes_in_bps below. 
    # Black Vol
    sigmas = np.array([0.4040, 0.3541, 0.3218, 0.3107, 0.3048, 0.2975, 0.2923, 0.2873, 0.2870])
    #The 'At the money volatility', corrosponding to a strike equal to the current forward price.
    atm_sigma = 0.3048
    #A list of strikes in bps (=0.0001) corrosponding to volatilites in sigmas
    strikes_in_bps = np.array([-150, -100, -50, -25, 0, 25, 50, 100, 150])
    #An inital guess of the parameters alpha, nu and rho.
    guess = [0.01, 10, -0.5]
    
    #calculating the actual strikes from f and strikes_in_bps
    strikes = f + strikes_in_bps*0.0001
    #Calling the SABR_calibration function defined below to return the parameters.
    alpha, nu, rho = SABR_calibration2(f, t_exp, atm_sigma, beta, strikes, sigmas, guess)
    
    #This nextsection of code simply draws a plot.
    Ks_in_bps = np.linspace(-150, 150, 60)
    Ks = f + Ks_in_bps*0.0001
    vols_from_Ks = SABR_market_vol(Ks, f, t_exp, alpha, beta, nu, rho)
    textbox = "\n".join((r"$\alpha=$"+f"{round(alpha,6)}",r"$\beta=$"+f"{beta}",
                        r"$\rho=$"+f"{round(rho,6)}", r"$\nu=$"+f"{round(nu,6)}"))
    fig, ax = plt.subplots()
    plt.plot(strikes_in_bps, sigmas, 'x')
    plt.plot(Ks_in_bps,vols_from_Ks)
    plt.xlabel("Strikes in bps")
    plt.ylabel("Market volatilities")
    plt.title(f"{t_exp} year into {tenor} year swaption")
    plt.text(0.6, 0.9, textbox, transform=ax.transAxes, fontsize=10,
        verticalalignment='top',bbox=dict(facecolor='white', alpha=0.7))
    
    #Saving the plot if desired.
    #plt.savefig(f"{t_exp} year into {tenor} year swaption"+".png")   
    

    
    
    
    