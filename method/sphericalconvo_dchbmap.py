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
class SphericalConvo_Gauss_2D:
    def __init__(self,dchbmap):
        self.dchbmap = dchbmap
        self.conv_dchbmap = [[0 for i in range(360)] for j in range(180)]
        self.kernel = int()
        self.sigma2 = float()
        self.gcff = float()
        self.points_kernel = list()
        self.fname = str()

    def read_kernel_txt(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()#1行目を読み飛ばし
            line = readfile.readline()#kernel値を読む
            linelist = list(line.split("="))
            self.kernel = int(linelist[1])
            for i in range(180):
                self.points_kernel.append(list())
                readfile.readline()
                line = readfile.readline()#kernel内にある座標点の個数を読む
                linelist = list(line.split("="))
                cnt = int(linelist[1])
                for j in range(cnt):
                    line = readfile.readline()
                    self.points_kernel[i].append(list(line.split(":")))

    def func_gauss_2D(self,centerx,centery,x,y):
        #fwhm = self.kerne#半値全幅はkernelそのもの
        self.sigma2 = self.kernel*self.kernel/2/math.log(2)#半値全幅をガウス関数のsigma(2乗値)に変換
        #self.gcff=1/2/math.pi/self.sigma2#2次元ガウス関数の係数#二次元正規化
        centery, y = centery%360, y%360
        #print(centery,y)
        #return self.gcff * np.exp(-((centerx-x)**2+(centery-y)**2)/self.sigma2/2)
        return np.exp(-((centerx-x)**2+(centery-y)**2)/self.sigma2/2)


    def spherical_convolution(self):
        deg = math.pi/180
        for i in tqdm(range(180)):
            for j in tqdm(range(360),leave=False):
                sum_points_dchb = 0
                sum_weight = 0
                #sum_gauss = 0
                if self.dchbmap[i][j] == 999.:
                    self.conv_dchbmap[i][j] =  999.
                    continue
                for pk in self.points_kernel[i]:
                    if self.dchbmap[int(pk[0])][(int(pk[1])+j)%360] == 999.:
                        continue
                    #本来は座標は89.5-lat,lon+0.5とするべきだが，
                    #ガウス関数内で2点の座標で差を取るため結局うち消える
                    #なので緯度経度の変換は行わなくてよい
                    gau = self.func_gauss_2D(centerx=i,centery=j,x=int(pk[0]),y=int(pk[1])+j)
                    #重み付けは畳み込むやつらの緯度に依存した重みだからiではなくpk[0]でつけるべきではないか?
                    # sum_points_dchb += self.dchbmap[int(pk[0])][(int(pk[1])+j)%360] * gau * math.cos((89.5-i)*deg)
                    # sum_weight += math.cos((89.5-i)*deg)*gau
                    #pk[0]version
                    sum_points_dchb += self.dchbmap[int(pk[0])][(int(pk[1])+j)%360] * gau * math.cos((89.5-int(pk[0]))*deg)
                    sum_weight += math.cos((89.5-int(pk[0]))*deg)*gau
                    #sum_gauss += gau
                    #print(f"-----{i}-{j}-{(pk[0])}-{str((int(pk[1])+j)%360)}")
                    #print(self.dchbmap[i][j], gau, math.cos((89.5-i)*deg), sum_points_dchb, sum_weight)
                self.conv_dchbmap[i][j] = sum_points_dchb / sum_weight
        return self.conv_dchbmap

    def save_convdchbmap(self,icr,fname,folder,exts):
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
                self.conv_dchbmap[i][j] = str(format(self.conv_dchbmap[i][j], ".6f"))
            #self.conv_dchbmap[i] = list(map(str, self.conv_dchbmap[i]))
        with open(filepath, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.conv_dchbmap)
        f.close()

#---------------------------------------------------------------------------
