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
class Draw_DCHBmap:
    def __init__(self):
        self.dchbmap = []

    def read_csv(self,fpath,adapt=1):
        self.dchbmap = []
        with open(fpath) as readfile:
            for i in range(180):
                line = readfile.readline()
                linelist = list(line.split(","))
                linelist[-1] = linelist[-1][:(len(linelist[-1])-1)]
                list_dchb = list(map(float, linelist))
                self.dchbmap.append(list_dchb)
                if adapt:
                    continue
                line = readfile.readline()
        return self.dchbmap

    def read_csv_adapt(self,fpath):
        self.dchbmap = []
        with open(fpath) as readfile:
            for i in range(180):
                line = readfile.readline()
                linelist = list(line.split(","))
                linelist[-1] = linelist[-1][:(len(linelist[-1])-1)]
                list_dchb = list(map(float, linelist))
                self.dchbmap.append(list_dchb)
                #line = readfile.readline()
        return self.dchbmap

    #dchbリストをradで用意しているので，degに変換する
    def rad_to_deg(self):
        rad = 180./math.pi
        list_after = list()
        for i in range(180):
            list_after.append(list())
            for j in range(360):
                x = self.dchbmap[i][j]*rad
                list_after[i].append(x)
        self.dchbmap = list_after

    def draw_dchbmap(self,icr,fname="figure title"):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])

        Z = list()
        for i in range(180):
            for j in range(360):
                if (self.dchbmap[i][j] > 900) or (self.dchbmap[i][j] < 0) :
                    print(f"error!! [{i},{j}]")
                Z.append(self.dchbmap[i][j])
        Z = np.array(Z)

        cm = plt.cm.get_cmap("jet_r")
        #データが欠損している部分(配列には0で格納されている)はグレーで表示
        #dchbmap作成時，データ欠損箇所は999の値として保存している -> make_dchbmap_adapt.py
        cm.set_over("0.8")
        cm.set_under("0.8")
        fig = plt.figure(figsize=(8,4))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        #axを設定
        ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
        #ax.set_title(fname)
        #ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("carrington longitude [deg]")
        ax.set_ylabel("heliographic latitude [deg]")
        ax.set_xlim([np.ndarray.min(X),np.ndarray.max(X)])
        ax.set_ylim([np.ndarray.min(Y),np.ndarray.max(Y)])
        ax.set_xticks(np.arange(0,420,60))
        ax.set_yticks(np.arange(-90,120,30))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        #print(np.ndarray.max(Z))
        maingraph=ax.scatter(X, Y, c=Z, vmin=0, vmax=25, s=35, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。

        #カラーバーを追加
        divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
        color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
        ticks = [i for i in range(-3,30,3)]
        colorbar=fig.colorbar(maingraph, cax=color_ax,ticks=ticks) #新しく作成したaxesであるcolor_axを渡す。

        print()
        print("if you want to continue to next work, please close the figure window.")
        plt.show()
#---------------------------------------------------------------------------
