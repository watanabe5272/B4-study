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

import function_EFACTOR as fEF
#---------------------------------------------------------------------------
class Expansion_Factor_Adapt:
    def __init__(self):
        self.r_photomag = [[0 for i in range(360)] for j in range(180)]
        self.r_sourcemag = [[0 for i in range(360)] for j in range(180)]
        self.efactormap = [[0 for i in range(360)] for j in range(180)]

    def read_rmag_adapt(self,fpath):
        cnt10 = 0
        cnt25 = 0
        errorlist = []
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
                    self.r_sourcemag[i][j] = list_s[3]
                    self.r_photomag[i][j] = list_p[3]
                    if list_p[0] == 1.0:
                        cnt10 += 1
                    elif list_p[0] == 2.5:
                        errorlist.append([i,j])
                        cnt25 += 1
            print(cnt10,cnt25)
            print(errorlist)
            for j in range(360):##1行分はこちらで補う
                self.r_sourcemag[179][j] = self.r_sourcemag[178][j]
                self.r_photomag[179][j] = self.r_photomag[178][j]

    def out_rmag_adapt(self):
        return self.r_photomag, self.r_sourcemag

    def make_efactormap(self):
        for i in range(180):
            for j in range(360):
                print("\n", f"[{i}, {j}]", self.r_photomag[i][j], self.r_sourcemag[i][j], end=" ")
                self.efactormap[i][j] = fEF.expansion_factor(photomag=self.r_photomag[i][j],sourcemag=self.r_sourcemag[i][j],photo=1.0,source=2.5)
                #print(self.efactormap[i][j])

    def out_efactormap(self):
        return self.efactormap

    def save_efactormap(self,icr,fname,folder,exts):
        ddir = os.getcwd()
        sep = os.sep
        today = dtime.now()
        todaynow = today.strftime("%Y%m%d%H%M%S")
        todaynow2 = todaynow[2:]
        todaynow3 = today.strftime("%Y-%m-%d %H:%M:%S")
        fname = fname + todaynow2 + exts
        filepath = ddir + sep + folder + sep + fname
        for i in range(180):
            for j in range(360):
                self.efactormap[i][j] = str(format(self.efactormap[i][j], ".5f"))#小数第3位までで切り捨て
        with open(filepath, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.efactormap)
        f.close()
#---------------------------------------------------------------------------
