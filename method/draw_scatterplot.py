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
from sklearn.linear_model import LinearRegression

ddir = os.getcwd()
sep = os.sep
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))
import function_DCHB as fDCHB
#---------------------------------------------------------------------------
class Draw_Scatterplot:
    def __init__(self):
        self.dchbmap = []
        self.swsips = []
        self.modelv = []
        self.fitfile = str()
        self.list_statics = [0 for i in range(6)]
        self.list_parameter = [0 for i in range(2)]
        self.increment = float()
        self.analysis = []
        self.mean = []
        self.stdiv = []
        self.increment_hori = float()
        self.analysis_hori = []
        self.mean_hori = []
        self.stdiv_hori = []
        self.sr_coef = float()
        self.sr_icpt = float()


    def set_modelv(self,modelv):
        self.modelv = modelv


    def set_dchbmap(self,dchbmap):
        self.dchbmap = dchbmap


    def set_swsips(self,swsips):
        self.swsips = swsips


    def draw_scatterplot(self,icr,fname="figure title"):
        X = np.array(self.dchbmap)
        Y = np.array(self.swsips)

        #cm = plt.cm.get_cmap("jet_r")
        fig = plt.figure(figsize=(10,7))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        #axを設定
        ax = fig.add_axes((0.1, 0.1, 0.85, 0.8))
        ax.set_title(fname)
        #ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("distance to coronal hole boundary [rad]")
        ax.set_ylabel("IPS solar wind speed [km/s]")
        ax.set_xlim([0,0.45])
        ax.set_ylim([200,900])
        ax.set_xticks(np.arange(0,0.50,0.05))
        ax.set_yticks(np.arange(200,950,50))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        maingraph=ax.scatter(X, Y, c="seagreen", s=0.2, alpha=0.8)

        #q = np.array([i*self.increment + self.increment/2 for i in range(len(self.analysis))])
        print("-----  choose additional option  -----")
        print("  [0]: nothing ")
        print("  [1]: value of mean and standard diviation by vertical binnng ")
        print("  [2]: value of mean and standard diviation by horizontal binnng ")
        print("  [3]: value of mean by horizontal and vertical binning each")
        choice = input("  -->  ")
        if choice == "0":
            pass
        elif choice == "1":
            self.analysis = np.array(self.analysis)
            self.analysis = self.analysis + self.increment/2
            self.mean = np.array(self.mean)
            self.stdiv = np.array(self.stdiv)
            ax.errorbar(self.analysis, self.mean, yerr=self.stdiv, capsize=3, fmt='o', markersize=5, ecolor='black', elinewidth=1.5, markeredgecolor="red", color='none')
        elif choice == "2":
            self.analysis_hori = np.array(self.analysis_hori)
            self.analysis_hori = self.analysis_hori + self.increment_hori/2
            self.mean_hori = np.array(self.mean_hori)
            self.stdiv_hori = np.array(self.stdiv_hori)
            ax.errorbar(self.mean_hori, self.analysis_hori, xerr=self.stdiv_hori, capsize=3, fmt='o', markersize=5, ecolor='black', elinewidth=1.5, markeredgecolor="blue", color='none')
        elif choice == "3":
            self.analysis = np.array(self.analysis)
            self.analysis = self.analysis + self.increment/2
            self.mean = np.array(self.mean)
            ax.plot(self.analysis, self.mean, mec='red', fillstyle='none', marker='o', markersize=5, linestyle='None', label="vertical")
            self.analysis_hori = np.array(self.analysis_hori)
            self.analysis_hori = self.analysis_hori + self.increment_hori/2
            self.mean_hori = np.array(self.mean_hori)
            ax.plot(self.mean_hori, self.analysis_hori, mec='blue', fillstyle="none", marker='o', markersize=5, linestyle='None', label="horizontal")

        p = np.linspace(0,1,360*5)
        #print("**************", self.list_parameter)
        ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=self.list_parameter[0],w=self.list_parameter[1]), c="magenta", label=f"eps={self.list_parameter[0]},w={self.list_parameter[1]}")
        ax.legend(loc='lower right')

        print()
        print("if you want to continue to next work, please close the figure window.")
        plt.show()


    def read_fittingresult_txt(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()
            self.fitfile = readfile.readline()
            for i in range(10):
                readfile.readline()
            for i in range(6):
                line = readfile.readline()
                #print(line[13:-1])
                self.list_statics[i] = float(line[13:-1])
            for i in range(2):
                readfile.readline()
            #epsilonの読み込み
            line = readfile.readline()
            self.list_parameter[0] = float(line[13:])
            #wの読み込み
            line = readfile.readline()
            self.list_parameter[1] = float(line[13:])
        return self.list_statics, self.list_parameter


    def read_scatteranalysis_txt(self,fpath):
        with open(fpath) as readfile:
            for i in range(8):
                readfile.readline()
            line = readfile.readline()
            linelist = list(line.split(":"))
            self.increment = float(linelist[1])
            for i in range(2):
                readfile.readline()
            j = 0
            while True:
                line = readfile.readline()
                if len(line)==0:
                    break
                linelist = list(line.split(":"))
                self.analysis.append(float(linelist[1]))#i値を格納
                line = readfile.readline()
                linelist = list(line.split(":"))
                self.mean.append(float(linelist[1]))#平均値を格納
                line = readfile.readline()
                linelist = list(line.split(":"))
                self.stdiv.append(float(linelist[1]))#標準偏差を格納
                j += 1

    def read_scatteranalysis_txt_hori(self,fpath):
        with open(fpath) as readfile:
            for i in range(8):
                readfile.readline()
            line = readfile.readline()
            linelist = list(line.split(":"))
            self.increment_hori = float(linelist[1])
            for i in range(2):
                readfile.readline()
            j = 0
            while True:
                line = readfile.readline()
                if len(line)==0:
                    break
                linelist = list(line.split(":"))
                self.analysis_hori.append(float(linelist[1]))#i値を格納
                line = readfile.readline()
                linelist = list(line.split(":"))
                self.mean_hori.append(float(linelist[1]))#平均値を格納
                line = readfile.readline()
                linelist = list(line.split(":"))
                self.stdiv_hori.append(float(linelist[1]))#標準偏差を格納
                j += 1


    def read_csv_adapt(self,fpath):
        with open(fpath) as readfile:
            for i in range(180):
                line = readfile.readline()
                linelist = list(line.split(","))
                linelist[-1] = linelist[-1][:(len(linelist[-1])-1)]
                list_modelv = list(map(float, linelist))
                self.modelv.append(list_modelv)

    def propotionalline(self, x):
        return x
        #y=xの直線を散布図に重ね書きしようと思った
        #相関係数は線形関係にあれば1に近づくのでy=axじゃないとだめ。
        #そのような直線の同定には最小二乗法を使うか?

    def single_regression(self):
        self.sr_coef = (self.list_statics[4])/(self.list_statics[2]**2)
        self.sr_icpt = self.list_statics[1] - self.sr_coef * self.list_statics[0]
        print(f"\ncoefficient : {self.sr_coef}")
        print(f"intercept : {self.sr_icpt}")

    def sr_line(self, x):
        return self.sr_coef * x + self.sr_icpt

    def draw_scatterplot_linear(self,icr,fname="figure title"):
        X = np.array(self.modelv)
        #print(len(X), len(X[-1]))
        #print(X[-1])
        #print(X[-2])
        Y = np.array(self.swsips)

        #cm = plt.cm.get_cmap("jet_r")
        fig = plt.figure(figsize=(8,8))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        #axを設定
        ax = fig.add_axes((0.1, 0.1, 0.85, 0.8))
        ax.set_title(fname)
        #ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("DCHB solar wind speed [km/s]")
        ax.set_ylabel("IPS solar wind speed [km/s]")
        ax.set_xlim([200,900])
        ax.set_ylim([200,900])
        ax.set_xticks(np.arange(200,950,50))
        ax.set_yticks(np.arange(200,950,50))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        maingraph=ax.scatter(X, Y, c="mediumblue", s=0.2, alpha=0.8)

        p = np.linspace(200,1000,360*5)
        ax.plot(p, self.propotionalline(x=p), c="slategrey", label=f"Y = X")
        #ax.plot(p, self.propotionalline(x=p), c="tomato", label=f"Y = X")

        ax.plot(p, self.sr_line(x=p), c="magenta", label=f"SR : {self.sr_coef:.3g} *X + {self.sr_icpt:.3g}")
        ax.legend(loc='lower right')

        print()
        print("if you want to continue to next work, please close the figure window.")
        plt.show()
#---------------------------------------------------------------------------
