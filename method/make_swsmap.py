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
import icrsetting
#---------------------------------------------------------------------------
class SWS:
    def __init__(self):
        self.swsmap = [[0 for i in range(360)] for j in range(180)]

    def read_dat(self,fpath):
        zero_cnt =0
        low2_cnt =0
        low_cnt =0
        with open(fpath) as readfile:
            for i in range(180):
                for j in range(360):
                    #IPS_SWSのデータは南北が反転していない
                    self.swsmap[i][j] = float(readfile.readline())
                    if self.swsmap[i][j]==0.:
                        zero_cnt +=1
                    if self.swsmap[i][j]>=200 and self.swsmap[i][j]<250:
                        low2_cnt +=1
                    if self.swsmap[i][j]>0 and self.swsmap[i][j]<200:
                        low_cnt +=1
        print(f"zero_count(invalid): {zero_cnt}")
        print(f"low2_count(200-250): {low2_cnt}")
        print(f"low_count(0-200): {low_cnt}")
        return self.swsmap

    def draw_swsmap(self,icr):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])

        Z = list()
        for i in range(180):
            for j in range(360):
                Z.append(self.swsmap[i][j])
        Z = np.array(Z)

        cm = plt.cm.get_cmap("jet_r").copy()
        cm.set_under("0.3")#データが欠損している部分(配列には0で格納されている)はグレーで表示
        fig = plt.figure(figsize=(8,4))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        #axを設定
        ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
        #ax.set_title(f"CR{icr} IPS-SWSmap")
        #ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("carrington longitude [deg]")
        ax.set_ylabel("heliographic latitude [deg]")
        ax.set_xlim([np.ndarray.min(X),np.ndarray.max(X)])
        ax.set_ylim([np.ndarray.min(Y),np.ndarray.max(Y)])
        ax.set_xticks(np.arange(0,420,60))
        ax.set_yticks(np.arange(-90,120,30))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        maingraph=ax.scatter(X, Y, c=Z, s=35, vmin=200, vmax=850, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。

        #maingraph=ax.scatter(X, Y, c=Z, s=35, vmin=300, vmax=900, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。

        #カラーバーを追加
        divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
        color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
        ticks = [i for i in range(0,1200,50)]
        colorbar = fig.colorbar(maingraph, cax=color_ax, ticks=ticks) #新しく作成したaxesであるcolor_axを渡す

        print()
        print("if you want to finish this program, please close the figure window.")
        plt.show()
#---------------------------------------------------------------------------
