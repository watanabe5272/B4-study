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
class CH_Boundary:
    def __init__(self):
        self.cl_mpdata = [[0 for i in range(360)] for j in range(180)]

    #KPVTもしくはGONGの磁場データを読みこんでopen/closeを判定した結果を戻り値とする
    #ADAPTはこのメソッドでは読みこめない
    def read_mpdata(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(179):#磁場データは179行分しかない
                for j in range(360):
                    line_p = readfile.readline()
                    line_s = readfile.readline()
                    list_p = list(map(float, line_p.split()))
                    list_s = list(map(float, line_s.split()))
                    if list_s[0]==2.5:
                        self.cl_mpdata[i][j] = 1
        for j in range(360):
            #1行分はこちらで補う
            #北極を1行追加するか，南極を追加するかが違う
            #現段階では，南極をこちらでコピーして追加している
            self.cl_mpdata[179][j] = self.cl_mpdata[178][j]
        return np.array(self.cl_mpdata)

    #CHBmapを表示する
    def draw_chbmap(self,icr=str()):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])
        Z = self.cl_mpdata

        fig = plt.figure(figsize=(8,4))
        plt.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'navy')

        plt.xlabel("carrington longitude (deg)")
        plt.ylabel("heliographic latitude (deg)")

        plt.xlim(0, 360)
        plt.ylim(-90, 90)

        plt.xticks(np.arange(0, 420, 60))
        plt.yticks(np.arange(-90, 120, 30))

        plt.minorticks_on()#刻み間隔って設定できる?

        plt.grid(which="major", color="gray", linewidth="0.3")
        plt.grid(which="minor", color="lightgray", linewidth="0.2", linestyle="-")

        #plt.title(f"CR{icr} CHB map")

        print("\nif you want to finish this program, please close the figure window.")
        plt.show()
#---------------------------------------------------------------------------
