import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
import function_PCC as fpcc
#---------------------------------------------------------------------------
class Fitting_MaxPCC:
    def __init__(self,swsips,dchbmap):
        self.swsips = swsips
        self.dchbmap = dchbmap
        self.kk_eps = 10
        self.kk_w = 10
        self.count = 0
        self.leflist_analysis = [0 for i in range(6)]
        self.leflist_parameter = [0,0]
        self.list_save = []
        self.sign_param = 99
        self.fig_X = []
        self.fig_Y = []
        self.fig_Z = []

    def set_increment(self):
        print("\nDefault increment of the epsilon (0.01 - 0.10):  10")
        if input("do you change this increment?  y or n  -->  ")=="y":
            self.kk_eps = int(input("input an increment number  -->  "))
        print("\nDefault increment of the w (0.01 - 0.10):  10")
        if input("do you change this increment?  y or n  -->  ")=="y":
            self.kk_w = int(input("input an increment number  -->  "))

    def fitting_maxpcc(self):
        for i in tqdm(range(1,self.kk_eps)):
            for j in tqdm(range(1,self.kk_w), leave=False):
                #ここの2重のforループでパラメータの全探索を行う
                Vf, Vs = 850, 200
                swsdchb = [[0 for _ in range(360)] for _ in range(180)]
                eps = 0.1 / self.kk_eps * i
                w = 0.1 / self.kk_w * j

                # if i==1 and j==1:
                #     pass
                # else:
                #     if eps < -1 or eps > 0.03:
                #         continue
                #     if w < -1 or w > 0.04:
                #         continue

                for k in range(180):
                    for l in range(360):
                        if (self.dchbmap[k][l] == 999.):#エラー除去
                            swsdchb[k][l] = 999.
                            continue
                        elif (self.dchbmap[k][l] == -1e8):#エラー除去
                            swsdchb[k][l] = -1e8
                            continue
                        else:#dchbmapの値からモデル速度を計算しswsdchbを作成
                            swsdchb[k][l] = fDCHB.dchbmodel(Vf=Vf,Vs=Vs,\
                            angular_d=self.dchbmap[k][l],eps=eps,w=w)
                            continue

                #DCHBモデルのSWSと，IPSのSWSとで相関係数などの統計値を計算
                # list_analysis = list(fpcc.weighted_PCC(swsdchb, self.swsips))
                list_analysis = list(fpcc.weighted_PCC_ElimError(swsdchb, self.swsips))

                #print(i, j, list_analysis[5])
                if i==1 and j==1:
                    self.leflist_analysis[5] = list_analysis[5]-1.
                #list_analysis[5]にはPCC値が入っているので，今より大きければ統計解析結果を更新
                if list_analysis[5] > self.leflist_analysis[5]:
                    self.leflist_analysis = list_analysis
                    #PCCが現時点で最大化させることができるパラメータ値を保存
                    self.leflist_parameter[0]=round(eps,self.kk_eps//10+1)
                    self.leflist_parameter[1]=round(w,self.kk_w//10+1)
        return self.leflist_analysis, self.leflist_parameter

    def print_fittingresult(self):
        print("\n***** fitting result *****")
        print(f"mean x     : {self.leflist_analysis[0]}")
        print(f"mean y     : {self.leflist_analysis[1]}")
        print(f"stdiv x    : {self.leflist_analysis[2]}")
        print(f"stdiv y    : {self.leflist_analysis[3]}")
        print(f"covariance : {self.leflist_analysis[4]}")
        print(f"PCC        : {self.leflist_analysis[5]}")
        print(f"\nepsilon    : {self.leflist_parameter[0]}")
        print(f"w          : {self.leflist_parameter[1]}\n")

    def save_fittingresult(self,icr,fname,folder,exts,filelist):
        today = dtime.now()
        todaynow = today.strftime("%Y%m%d%H%M%S")
        todaynow2 = todaynow[2:]
        todaynow3 = today.strftime("%Y-%m-%d %H:%M:%S")
        fname = fname + todaynow2 + exts
        filepath = ddir + sep + folder + sep + fname
        with open(filepath,"w") as f:
            f.write(f"the result of maximizing PCC fitting\n")
            f.write(f"{fname}\n\n")
            f.write(f"{filelist[0]}\n")
            f.write(f"{filelist[1]}\n\n")
            f.write(f"current time      : {todaynow3}\n")
            f.write(f"CR                : {icr}\n")
            f.write(f"epsilon increment : {self.kk_eps}\n")
            f.write(f"w       increment : {self.kk_w}\n\n")
            f.write("***** statistic data *****\n")
            f.write(f"mean x     : {self.leflist_analysis[0]}\n")
            f.write(f"mean y     : {self.leflist_analysis[1]}\n")
            f.write(f"stdiv x    : {self.leflist_analysis[2]}\n")
            f.write(f"stdiv y    : {self.leflist_analysis[3]}\n")
            f.write(f"covariance : {self.leflist_analysis[4]}\n")
            f.write(f"PCC        : {self.leflist_analysis[5]}\n\n")
            f.write("***** fitted parameter *****\n")
            f.write(f"epsilon    : {self.leflist_parameter[0]}\n")
            f.write(f"w          : {self.leflist_parameter[1]}")
        f.close()


    def oneparam_pcc(self):
        Vf, Vs = 850, 200
        swsdchb = [[0 for i in range(360)] for j in range(180)]
        eps = float(input("input the value 'epsilon'  -->  "))
        w = float(input("input the value    'w'     -->  "))

        self.leflist_parameter[0] = eps
        self.leflist_parameter[1] = w

        for k in range(180):
            for l in range(360):
                swsdchb[k][l] = fDCHB.dchbmodel(Vf=Vf,Vs=Vs,\
                angular_d=self.dchbmap[k][l],eps=eps,w=w)

        list_analysis = list(fpcc.weighted_PCC(x=swsdchb,y=self.swsips))
        self.leflist_analysis = list_analysis

    def transition_pcc(self):
        self.sign_param = int(input("which parameter do you fix?\n  [0] epsilon  [1] w    -->  "))
        if self.sign_param==0:
            eps = float(input("input the value 'epsilon'  -->  "))
            self.kk_eps =  0.0
            self.kk_w = int(input("input an increment : default is 10 -->  "))
            self.count = self.kk_w
            for j in tqdm(range(1,self.kk_w), leave=True):
                Vf, Vs = 850, 200
                swsdchb = [[0 for i in range(360)] for j in range(180)]
                w = 0.1 / self.kk_w * j

                for k in range(180):
                    for l in range(360):
                        #dchbmapの値からモデル速度を計算しswsdchbを作成
                        swsdchb[k][l] = fDCHB.dchbmodel(Vf=Vf,Vs=Vs,\
                        angular_d=self.dchbmap[k][l],eps=eps,w=w)

                list_parameter=[eps,w]
                list_analysis=list(fpcc.weighted_PCC(x=swsdchb,y=self.swsips))
                self.list_save.append(list())
                self.list_save[-1].append(list_parameter[0])
                self.list_save[-1].append(list_parameter[1])
                self.list_save[-1].append(list_analysis[5])

        elif self.sign_param==1:
            w = float(input("input the value    'w'     -->  "))
            self.kk_eps = int(input("input an increment : default is 10 -->  "))
            self.kk_w =  0.0
            self.count = self.kk_eps

            for i in tqdm(range(1,self.kk_eps), leave=True):
                Vf, Vs = 850, 200
                swsdchb = [[0 for i in range(360)] for j in range(180)]
                eps = 0.1 / self.kk_eps * i

                for k in range(180):
                    for l in range(360):
                        #dchbmapの値からモデル速度を計算しswsdchbを作成
                        swsdchb[k][l] = fDCHB.dchbmodel(Vf=Vf,Vs=Vs,\
                        angular_d=self.dchbmap[k][l],eps=eps,w=w)

                list_parameter=[eps,w]
                list_analysis=list(fpcc.weighted_PCC(x=swsdchb,y=self.swsips))
                self.list_save.append(list())
                self.list_save[-1].append(list_parameter[0])
                self.list_save[-1].append(list_parameter[1])
                self.list_save[-1].append(list_analysis[5])
                # print(list_parameter)
                # print(list_analysis)
                # print(self.list_save)

    def save_fixingresult(self,icr,fname,folder,exts):
        today = dtime.now()
        todaynow = today.strftime("%Y%m%d%H%M%S")
        todaynow2 = todaynow[2:]
        todaynow3 = today.strftime("%Y-%m-%d %H:%M:%S")
        fname = fname + todaynow2 + exts
        filepath = ddir + sep + folder + sep + fname
        with open(filepath,"w") as f:
            f.write(f"the result of paramfixing PCC\n")
            f.write(f"{fname}\n\n")
            f.write(f"current time      : {todaynow3}\n")
            f.write(f"CR                : {icr}\n")
            f.write(f"epsilon increment : {self.kk_eps}\n")
            f.write(f"w       increment : {self.kk_w}\n\n")
            for i in range(self.count-1):
                f.write(f"epsilon : {self.list_save[i][0]}\n")
                f.write(f"w       : {self.list_save[i][1]}\n")
                f.write(f"PCC     : {self.list_save[i][2]}\n\n")
        f.close()

    def draw_fixingresult(self):
        X_eps = np.array([x[0] for x in self.list_save])
        Y_w   = np.array([x[1] for x in self.list_save])
        Z_pcc = np.array([x[2] for x in self.list_save])

        #cm = plt.cm.get_cmap("jet_r")
        fig = plt.figure(figsize=(8,4))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1

        if self.sign_param == 0:
            #axを設定
            ax = fig.add_axes((0.1, 0.13, 0.8, 0.8))
            ax.set_title("")
            #ax.grid(Falth)#グリッド線を追加
            ax.set_xlabel("w [rad]")
            ax.set_ylabel("PCC")
            ax.set_xlim([0,0.1])
            ax.set_ylim([0,1])
            ax.set_xticks(np.arange(0,0.11,0.01))
            ax.set_yticks(np.arange(0,1.1,0.1))
            ax.grid(True, linewidth=0.7, alpha=0.7)

            maingraph=ax.plot(Y_w, Z_pcc, linewidth=0.8, c="red")

            #p = np.linspace(0,1,360*5)
            #print("**************", self.list_parameter)
            # ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=self.list_parameter[0],w=self.list_parameter[1]), c="magenta", label=f"eps={self.list_parameter[0]},w={self.list_parameter[1]}")
            # ax.legend(loc='lower right')

            print()
            print("if you want to continue to next work, please close the figure window.")
            plt.show()
        elif self.sign_param == 1:
            #axを設定
            ax = fig.add_axes((0.13, 0.13, 0.8, 0.8))
            ax.set_title("")
            #ax.grid(Falth)#グリッド線を追加
            ax.set_xlabel("epsilon [rad]")
            ax.set_ylabel("PCC")
            ax.set_xlim([0,0.1])
            ax.set_ylim([0,1])
            ax.set_xticks(np.arange(0,0.11,0.01))
            ax.set_yticks(np.arange(0,1.1,0.1))
            ax.grid(True, linewidth=0.7, alpha=0.7)

            maingraph=ax.plot(X_eps, Z_pcc, linewidth=0.8, c="red")

            #p = np.linspace(0,1,360*5)
            #print("**************", self.list_parameter)
            # ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=self.list_parameter[0],w=self.list_parameter[1]), c="magenta", label=f"eps={self.list_parameter[0]},w={self.list_parameter[1]}")
            # ax.legend(loc='lower right')

            print()
            print("if you want to continue to next work, please close the figure window.")
            plt.show()

    def read_fixingtxt(self, fpath):
        with open(fpath) as readfile:
            readfile.readline()
            self.fitfile = readfile.readline()
            for i in range(3):
                readfile.readline()

            #incrementの読み込み
            list_inc = []
            for i in range(2):
                line = readfile.readline()
                #print(line[13:-1])
                list_inc.append(float(line[20:-1]))

            #空行1行を読み飛ばし
            readfile.readline()

            #pccの推移を読み込み
            self.fig_X.append(list())
            self.fig_Y.append(list())
            self.fig_Z.append(list())
            for i in range(int(max(list_inc))-1):
                line = readfile.readline()
                self.fig_X[-1].append(float(line[11:-1]))
                line = readfile.readline()
                self.fig_Y[-1].append(float(line[11:-1]))
                line = readfile.readline()
                self.fig_Z[-1].append(float(line[11:-1]))
                line = readfile.readline()


    def draw_multi_fixingresult(self,list_title):
        X_eps = np.array(self.fig_X)
        Y_w   = np.array(self.fig_Y)
        Z_pcc = np.array(self.fig_Z)

        #cm = plt.cm.get_cmap("jet_r")
        fig = plt.figure(figsize=(8,4))
        #plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1

        if self.sign_param == 0:
            #axを設定
            ax = fig.add_axes((0.1, 0.13, 0.8, 0.8))
            ax.set_title("")
            #ax.grid(Falth)#グリッド線を追加
            ax.set_xlabel("w [rad]")
            ax.set_ylabel("PCC")
            ax.set_xlim([0,0.1])
            ax.set_ylim([0,1])
            ax.set_xticks(np.arange(0,0.11,0.01))
            ax.set_yticks(np.arange(0,1.1,0.1))
            ax.tick_params(axis="both", labelsize=8)
            ax.grid(True, linewidth=0.7, alpha=0.7)

            for i in range(len(Y_w)):
                maingraph=ax.plot(Y_w[i], Z_pcc[i], linewidth=0.8, c=cm.jet((i+1)/(len(Y_w)+1)),label=list_title[i])

            ax.legend(ncol=2, loc='lower right')

            print()
            print("if you want to continue to next work, please close the figure window.")
            plt.show()

        elif self.sign_param == 1:
            #axを設定
            ax = fig.add_axes((0.1, 0.13, 0.8, 0.8))
            ax.set_title("")
            #ax.grid(Falth)#グリッド線を追加
            ax.set_xlabel("epsilon [rad]")
            ax.set_ylabel("PCC")
            ax.set_xlim([0,0.1])
            ax.set_ylim([0,1])
            ax.set_xticks(np.arange(0,0.11,0.01))
            ax.set_yticks(np.arange(0,1.1,0.1))
            ax.tick_params(axis="both", labelsize=8)
            ax.grid(True, linewidth=0.7, alpha=0.7)

            for i in range(len(X_eps)):
                maingraph=ax.plot(X_eps[i], Z_pcc[i], linewidth=0.8, c=cm.jet((i+1)/(len(X_eps)+1)),label=list_title[i])

            ax.legend(ncol=2, loc='lower right')

            print()
            print("if you want to continue to next work, please close the figure window.")
            plt.show()
#---------------------------------------------------------------------------
