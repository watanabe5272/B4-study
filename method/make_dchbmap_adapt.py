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
class Distance_CHB_Adapt:
    def __init__(self,mpdata):
        self.mpdata = mpdata
        self.theta_pl = [[0 for i in range(360)] for j in range(180)]
        self.phi_pl = [[0 for i in range(360)] for j in range(180)]
        self.dchbmap = list()

    #2.5Rsの磁力線のフットポイントの緯度をtheta_plとして，経度をphi_plとして返す
    def read_photoloc_adapt(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(179):#磁場データは179行分しかない
                for j in range(360):
                    readfile.readline()#theta, phiの情報を1行分読み飛ばす
                    countline = readfile.readline()
                    countlist = list(countline.split("="))
                    countnum = int(countlist[1])
                    line_s = readfile.readline()
                    for k in range(countnum-1):#途中計算は読み飛ばす
                        readfile.readline()
                    line_p = readfile.readline()
                    list_s = list(map(float, line_s.split()))
                    list_p = list(map(float, line_p.split()))
                    if list_p[0] == 1.0:
                        self.theta_pl[i][j] = list_p[1]
                        self.phi_pl[i][j] = list_p[2]
                    elif list_p[0] == 2.5:#ncount=1で計算エラーデータには-1e8を入れておく
                        self.theta_pl[i][j] = -1e8
                        self.phi_pl[i][j] = -1e8

            for j in range(360):##1行分はこちらで補う
                self.theta_pl[179][j] = self.theta_pl[178][j]
                self.phi_pl[179][j] = self.phi_pl[178][j]
        return self.theta_pl, self.phi_pl
#---------------------------------------------------------------------------
