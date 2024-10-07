import pandas as pd
import numpy as np
import statsmodels.regression
import statsmodels.api as sm
from scipy import stats
 

#доверительный интервал для функции регрессии Mx(y)
def numpynterval_exp(x_matrix, x0, mse, regr_coefs, alpha=0.95):
    y = sum(x0*regr_coefs)
    t = stats.t.ppf(alpha, x_matrix.shape[0]-x_matrix.shape[1]-1)
    S = mse*np.sqrt(x0.T@np.linalg.inv(x_matrix.T@x_matrix)@x0)
    
    left = y-t*S
    right = y+t*S
    
    return (left, right)


#доверительный интервал для значений функции регрессии y
def conf_interval_values(x_matrix, x0, mse, regr_coefs, alpha=0.95):
    y = sum(x0*regr_coefs)
    t = stats.t.ppf(alpha, x_matrix.shape[0]-x_matrix.shape[1]-1)
    S = mse*np.sqrt(1+x0.T@np.linalg.inv(x_matrix.T@x_matrix)@x0)
    
    left = y-t*S
    right = y+t*S
    
    return (left, right)


#доверительный интервал дисперсии возмущений
def conf_interval_var(x_matrix, mse, alpha=0.95):
    a_left = (1-alpha)/2
    a_right = alpha+(1-alpha)/2
    chi_left = stats.chi2.ppf(a_left, x_matrix.shape[0]-x_matrix.shape[1])
    chi_right = stats.chi2.ppf(a_right, x_matrix.shape[0]-x_matrix.shape[1])
    
    n = x_matrix.shape[0]
    left = (n*mse)/chi_left
    right = (n*mse)/chi_right
    
    return (right, left)


#коэффициент эластичности
def elastic_correction(reg_coefs, x_matrix, y):
    x_mean = x_matrix.mean()
    y_mean = y.mean()
    E = reg_coefs*x_mean/y_mean
    
    return E


#Доверительный интервал M(x) (Парная регресси)
def linear_conf_interval_exp(x_vals, x0, y0, mse, alpha=0.95):
    S_y = mse*(1/x_vals.shape[0]+ ((x0-x_vals.mean())**2 / (((x_vals-x_vals.mean())**2).sum())))
    t = stats.t.ppf(alpha, x_vals.shape[0]-2)
    
    left = y0-t*np.sqrt(S_y)
    right = y0+t*np.sqrt(S_y)

    return (left, right)


#Доверительный интервал y0 (Парная регресси)
def linear_conf_interval_val(x_vals, x0, y0, mse, alpha=0.95):
    S_y = mse*(1 + 1/x_vals.shape[0] + ((x0-x_vals.mean())**2 / (((x_vals-x_vals.mean())**2).sum())))
    t = stats.t.ppf(alpha, x_vals.shape[0]-2)
    
    left = y0-t*np.sqrt(S_y)
    right = y0+t*np.sqrt(S_y)

    return (left, right)