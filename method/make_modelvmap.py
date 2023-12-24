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

#実行ファイルのあるディレクトリ内のデータフォルダを検索範囲に追加する
ddir = os.getcwd()
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))
import function_DCHB as fDCHB
import function_WSA as fWSA
#---------------------------------------------------------------------------
class Make_Modelvmap:
    def __init__(self,dchbmap,eps,w):
        self.dchbmap = np.array(dchbmap)
        self.efactormap = []
        self.modelvmap = [[0 for i in range(360)] for j in range(180)]
        self.Vf, self.Vs = 850, 200
        self.eps, self.w = eps, w
        self.EUHFORIA = {"alpha":0.222,"beta":1.0,"gamma":0.8,"delta":1.25,"w":0.02,"k":3,"Vf":915,"Vs":240}

    def set_efactormap(self,efactormap):
        self.efactormap = np.array(efactormap)


    def make_modelvmap(self):
        self.modelvmap = fDCHB.dchbmodel(Vf=self.Vf,Vs=self.Vs,angular_d=self.dchbmap,eps=self.eps,w=self.w)
        for i in range(180):
            for j in range(360):
                if self.dchbmap[i][j] == 999.:
                    self.modelvmap[i][j] = 999.


    def make_wsamap(self):
        #print(type(self.EUHFORIA["Vf"]))
        for i in range(180):
            for j in range(360):
                self.modelvmap[i][j] = fWSA.wsamodel(Vf=self.EUHFORIA["Vf"],Vs=self.EUHFORIA["Vs"],e_factor=self.efactormap[i][j],angular_d=self.dchbmap[i][j],alpha=self.EUHFORIA["alpha"],delta=self.EUHFORIA["delta"],w=self.EUHFORIA["w"],k=self.EUHFORIA["k"],beta=self.EUHFORIA["beta"],gamma=self.EUHFORIA["gamma"])



    def draw_modelvmap(self,icr,fname="figure title"):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])

        Z = list()
        for i in range(180):
            for j in range(360):
                Z.append(self.modelvmap[i][j])
        Z = np.array(Z)

        cm = plt.cm.get_cmap("jet_r")
        #cm = plt.cm.get_cmap("gray")
        cm.set_over("1.0")
        cm.set_under("1.0")
        fig = plt.figure(figsize=(8,4))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        #axを設定
        ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
        ax.set_title(fname, fontsize=12)
        #ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("Carrington longitude [deg]")
        ax.set_ylabel("heliographic latitude [deg]")
        ax.set_xlim([np.ndarray.min(X),np.ndarray.max(X)])
        ax.set_ylim([np.ndarray.min(Y),np.ndarray.max(Y)])
        ax.set_xticks(np.arange(0,420,60))
        ax.set_yticks(np.arange(-90,120,30))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        #print(np.ndarray.max(Z))
        maingraph=ax.scatter(X, Y, c=Z, vmin=200, vmax=850, s=35, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。
        #カラーバーを追加
        divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
        color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
        ticks = [i for i in range(200,900,50)]
        #colorbar=fig.colorbar(maingraph, cax=color_ax, ticks=ticks) #新しく作成したaxesであるcolor_axを渡す。
        colorbar=fig.colorbar(maingraph, cax=color_ax, ticks=ticks)
        colorbar.set_label("[km/s]",loc="center",rotation=270, fontsize=12, labelpad=14)

        print()
        print("if you want to continue to next work, please close the figure window.")
        plt.show()
        plt.savefig("figure_cr1913.eps",format="eps")


    def save_modelvmap(self,icr,fname,folder,exts):
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
                self.modelvmap[i][j] = str(format(self.modelvmap[i][j], ".3f"))#小数第3位までで切り捨て
            #self.conv_dchbmap[i] = list(map(str, self.conv_dchbmap[i]))
        with open(filepath, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.modelvmap)
        f.close()

    def round_speed(self):
        for i in range(180):
            for j in range(360):
                if self.modelvmap[i][j] > 850:
                    print(i, j, "over!")
                    self.modelvmap[i][j] = 851.0
                elif self.modelvmap[i][j] < 200:
                    print(i, j, "under!")
                    self.modelvmap[i][j] = 200.0
#---------------------------------------------------------------------------
