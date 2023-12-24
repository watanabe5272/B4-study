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
class Convo_Gauss_2D:
    def __init__(self,dchbmap):
        self.dchbmap = dchbmap
        self.dchbmap_array = np.array(0)
        self.filter = list()
        self.filter_array = np.array(0)


    def convolution(self,oddangle=int(15)):#angleには奇数を入れる
        #まずフィルター配列を準備する
        self.filter = [[0 for i in range(oddangle)] for j in range(oddangle)]
        fwhm=oddangle/2#半値全幅
        sigma2=fwhm*fwhm/8/math.log(2)#sigmaの2乗
        gcff=1/2/math.pi/sigma2#2次元ガウス関数の係数
        fil_wid = int((oddangle-1)//2)
        for i in range(oddangle):
            for j in range(oddangle):
                x=(i-fil_wid)**2+(j-fil_wid)**2
                self.filter[i][j]=gcff*np.exp(-x/sigma2/2)
        #フィルターと元のdchbmapをarray化
        self.filter_array =  np.array(self.filter)
        self.dchbmap_array = np.array(self.dchbmap)
        #scipyのメソッドを使ってコンボリューションをかける
        #コンボリューションのmodeをfullで行うと，配列が拡大する
        corrdchb=signal.correlate2d(in1=self.dchbmap_array,in2=self.filter_array,mode="full")
        #拡大した配列を整形して180*360に戻す
        corrdchb_all = []
        for i in range(fil_wid,len(corrdchb)-fil_wid):
            x = list(corrdchb[i])
            corrdchb_all.append(x[fil_wid:-fil_wid])
        self.dchbmap_array = corrdchb_all
        #戻り値の型はlistであることに注意
        return self.dchbmap_array
#---------------------------------------------------------------------------
