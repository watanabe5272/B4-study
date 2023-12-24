import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import csv
from scipy import signal
from tqdm import tqdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime
#---------------------------------------------------------------------------
deg = math.pi/180

def RMSEandMEANBIAS(f_model, y_obs):#RMSEと規格化RMSEとMEANBIASを戻り値とする
    g = 0
    sum_G = 0
    diviation,diviationsum,diviationsqare,diviationsqaresum = 0,0,0,0
    RMSE, normalizedRMSE = 0, 0
    MEANBIAS = 0
    for i in range(180):
        g = math.cos((89.5-i)*deg)
        for j in range(360):
            diviation = f_model[i][j] -  y_obs[i][j]
            diviationsum += diviation
            diviationsqare = diviation ** 2
            diviationsqaresum += diviationsqare
            sum_G += g
    MEANBIAS = diviationsum / sum_G
    RMSE = math.sqrt(diviationsqaresum / sum_G)

    obsmax,obsmin,tmpmax,tmpmin = 0,0,0,0
    for i in range(180):
        # print(type(y_obs[i]),len(y_obs[i]))
        # print(y_obs[i])
        # print(max(y_obs[i]))
        tmpmax, tmpmin = max(y_obs[i]), min(y_obs[i])
        if i == 0:
            obsmax, obsmin = tmpmax, tmpmin
            continue
        if obsmax < tmpmax:
            obsmax = tmpmax
        if obsmin > tmpmin:
            obsmin = tmpmin

    normalizedRMSE = RMSE/(obsmax-obsmin)

    return RMSE, normalizedRMSE, MEANBIAS
#---------------------------------------------------------------------------
