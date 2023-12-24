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
def weighted_PCC(x, y):
    X, Y = [], []
    for i in range(180):
        for j in range(360):
            X.append(x[i][j]), Y.append(y[i][j])
    X, Y = np.array(X), np.array(Y)

    #重み付き総和を計算
    sum_X, sum_Y, sum_G = 0, 0, 0
    list_g = []
    #errornum = []
    deg = math.pi/180
    for i in range(180):
        g = math.cos((89.5-i)*deg)
        list_g.append(g)
        for j in range(360):
            h = i*360+j
            # if X[h] == 999. or Y[h] == 999.:
            #     errornum.append(h)
            #     continue
            sum_X += X[h]*g
            sum_Y += Y[h]*g
            sum_G += g

    #重み付き平均値を計算
    mean_X, mean_Y = sum_X/sum_G, sum_Y/sum_G

    #残差を計算
    diff_X, diff_Y = X-mean_X, Y-mean_Y
    #重み付き残差の2乗を計算
    diffsq_X, diffsq_Y = diff_X**2, diff_Y**2
    #print(diffsq_X)
    for i in range(180):
        for j in range(360):
            h = i*360+j
            diffsq_X[h] *= list_g[i]
            diffsq_Y[h] *= list_g[i]

    # for i in errornum:
    #     diff_X[h] = -999.
    #     diff_Y[h] = -999.
    #     diffsq_X[h] = -999.
    #     diffsq_Y[h] = -999.

    #標準偏差を計算
    stdiv_X = np.sqrt(np.sum(diffsq_X)/sum_G)
    stdiv_Y = np.sqrt(np.sum(diffsq_Y)/sum_G)

    #共分散を計算
    sum_C = 0
    for i in range(180):
        for j in range(360):
            h = i*360+j
            sum_C += diff_X[h] * diff_Y[h] * list_g[i]
    covariance = sum_C/sum_G

    #重み付き相関係数を計算
    pcc = covariance / stdiv_X / stdiv_Y

    return mean_X, mean_Y, stdiv_X, stdiv_Y, covariance, pcc
#---------------------------------------------------------------------------
def weighted_PCC_ElimError(dchb_x, ips_y):

    #重み付き総和を計算
    sum_X, sum_Y, sum_G = 0, 0, 0
    list_g = []
    errornum_dchb = []
    errornum_ips = []
    deg = math.pi/180

    for i in range(180):
        g = math.cos((89.5-i)*deg)#緯度依存重み
        for j in range(360):
            if dchb_x[i][j] == 999. or dchb_x[i][j] == -1e8:
                errornum_dchb.append([i, j])
                continue
            if ips_y[i][j] == 999. or ips_y[i][j] == 0.:
                errornum_ips.append([i, j])
                continue
            sum_X += dchb_x[i][j]*g
            sum_Y += ips_y[i][j]*g
            sum_G += g

    #重み付き平均値を計算
    mean_X, mean_Y = sum_X/sum_G, sum_Y/sum_G

    #残差を計算
    diff_X = [[0 for i in range(360)] for j in range(180)]
    diff_Y = [[0 for i in range(360)] for j in range(180)]
    for i in range(180):
        for j in range(360):
            if dchb_x[i][j] == 999. or dchb_x[i][j] == -1e8:
                diff_X[i][j] = dchb_x[i][j]
            if ips_y[i][j] == 999. or ips_y[i][j] == 0.:
                diff_Y[i][j] = ips_y[i][j]
            diff_X[i][j] = dchb_x[i][j] - mean_X
            diff_Y[i][j] = ips_y[i][j] - mean_Y

    diff_X = np.array(diff_X)
    diff_Y = np.array(diff_Y)

    #重み付き残差の2乗を計算
    diffsq_X, diffsq_Y = diff_X**2, diff_Y**2

    for i in range(180):
        g = math.cos((89.5-i)*deg)#緯度依存重み
        for j in range(360):
            diffsq_X[i][j] *= g
            diffsq_Y[i][j] *= g

    for x in errornum_dchb:
        diff_X[x[0]][x[1]] = 0
        diffsq_X[x[0]][x[1]] = 0
    for x in errornum_ips:
        diff_Y[x[0]][x[1]] = 0
        diffsq_Y[x[0]][x[1]] = 0


    #標準偏差を計算  #エラー値は0にしたのでsumをとることで自動的に無視される
    stdiv_X = np.sqrt(np.sum(diffsq_X)/sum_G)
    stdiv_Y = np.sqrt(np.sum(diffsq_Y)/sum_G)


    #共分散を計算
    sum_C = 0
    for i in range(180):
        g = math.cos((89.5-i)*deg)#緯度依存重み
        for j in range(360):
            sum_C += diff_X[i][j] * diff_Y[i][j] * g
    covariance = sum_C/sum_G

    #重み付き相関係数を計算
    pcc = covariance / stdiv_X / stdiv_Y

    return mean_X, mean_Y, stdiv_X, stdiv_Y, covariance, pcc
#---------------------------------------------------------------------------
#**********************************************************
#**********************************************************
#                      直しきった！はず！
#**********************************************************
#**********************************************************
