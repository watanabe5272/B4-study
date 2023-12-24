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

ddir = os.getcwd()
sep = os.sep
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))
import function_DCHB as fDCHB
#---------------------------------------------------------------------------
class Draw_DCHBmap_onPhoto:
    def __init__(self,chbmap,dchbmap,theta,phi):
        self.chbmap = chbmap
        self.dchbmap = dchbmap
        # self.onphoto = [[[[0,0]] for i in range(360)] for j in range(180)]
        self.onphoto = [[[] for i in range(360)] for j in range(180)]
        self.theta = theta
        self.phi = phi

    def make_dchbmap_onphoto(self):
        deg = math.pi/180
        for i in range(180):
            for j in range(360):
                if round(self.theta[i][j])==180:
                    t = 0
                else:
                    t = round(self.theta[i][j])
                if round(self.phi[i][j])==360:
                    p = 0
                else:
                    p = round(self.phi[i][j])
                #print(t, p)

                self.onphoto[t][p].append([self.dchbmap[i][j],i])
        for i in range(180):
            for j in range(360):
                sum = 0
                sumg = 0
                for x in self.onphoto[i][j]:
                    #print(x)
                    #print(x[0], x[1])
                    sum += x[0]*math.cos((89.5-x[1])*deg)
                    sumg += math.cos((89.5-x[1])*deg)
                self.onphoto[i][j] = sum/sumg

        #closedな領域をグレーで書き出したい。
        #drawメソッドの，「cm.set_under("0.7")」に関連している
        for i in range(180):
            for j in range(360):
                if self.onphoto[i][j]==0:
                    self.onphoto[i][j]=100


    def draw_dchbmap_onphoto(self,icr,fname="figure title"):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])
        Z = list()
        for i in range(180):
            for j in range(360):
                Z.append(self.onphoto[i][j])
        Z = np.array(Z)

        cm = plt.cm.get_cmap("jet_r").copy()
        cm.set_over("0.7")
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

        maingraph=ax.scatter(X, Y, c=Z, vmin=0, vmax=25, s=35, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。
        Z = self.chbmap
        ax.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'navy')
        #カラーバーを追加
        divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
        color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
        ticks = [i for i in range(-3,30,3)]
        colorbar=fig.colorbar(maingraph, cax=color_ax,ticks=ticks) #新しく作成したaxesであるcolor_axを渡す。
        print("\nif you want to finish this program, please close the figure window.")
        plt.show()
#---------------------------------------------------------------------------
