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
# ---------------------------------------------------------------------------


class CH_Boundary_Adapt:
    def __init__(self):
        self.cl_mpdata = [[0 for i in range(360)] for j in range(180)]
        self.cl_mpdata_sinlat = [[0 for i in range(360)] for j in range(180)]

    # KPVTもしくはGONGの磁場データを読みこんでopen/closeを判定した結果を戻り値とする
    # ADAPTはこのメソッドでは読みこめない
    def read_mpdata_adapt(self, fpath):
        ss = float(input("\ninput the Source Surface altitude you choosed  -->  "))
        with open(fpath) as readfile:
            readfile.readline()
            readfile.readline()  # 先頭2行を読み飛ばし
            for i in range(179):  # 磁場データは179行分しかない
                for j in range(360):
                    readfile.readline()  # theta, phiの情報を1行分読み飛ばす
                    countline = readfile.readline()
                    countlist = list(countline.split("="))
                    countnum = int(countlist[1])
                    line_p = readfile.readline()
                    for k in range(countnum-1):
                        readfile.readline()  # 途中計算を読み飛ばす
                    line_s = readfile.readline()
                    list_p = list(map(float, line_p.split()))
                    list_s = list(map(float, line_s.split()))
                    if list_s[0] == ss:
                        self.cl_mpdata[i][j] = 1

        for j in range(360):
            # 1行分はこちらで補う
            # 北極を1行追加するか，南極を追加するかが違う
            # 現段階では，南極をこちらでコピーして追加している
            self.cl_mpdata[179][j] = self.cl_mpdata[178][j]

        # そのままだと穴があるので，緯度75deg以上は全てopen磁場とする
        # for i in range(15):
        #    for j in range(360):
        #        self.cl_mpdata[i][j] = 1
        #        self.cl_mpdata[179-i][j] = 1

        return np.array(self.cl_mpdata)

    def toSineLatitude(self):
        radtodeg = 180 / math.pi
        for i in range(180):
            for j in range(360):
                lat = round(math.asin((i - 89.5)/90) * radtodeg + 89.5)
                self.cl_mpdata_sinlat[i][j] = self.cl_mpdata[lat][j]
            # print(i, lat)

    # CHBmapを表示する

    def draw_chbmap_adapt(self, icr=str()):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89, -91, -1)])
        Z = self.cl_mpdata

        fig = plt.figure(figsize=(8, 4))
        plt.contour(X, Y, Z, linewidths=0.7, levels=0, colors='navy')

        plt.xlabel("carrington longitude (deg)")
        plt.ylabel("heliographic latitude (deg)")

        plt.xlim(0, 360)
        plt.ylim(-90, 90)

        plt.xticks(np.arange(0, 420, 60))
        plt.yticks(np.arange(-90, 120, 30))

        plt.minorticks_on()  # 刻み間隔って設定できる?

        plt.grid(which="major", color="gray", linewidth="0.3")
        plt.grid(which="minor", color="lightgray",
                 linewidth="0.2", linestyle="-")

        # plt.title(f"CR{icr} CHB map")

        print("\nif you want to finish this program, please close the figure window.")
        plt.show()

    def draw_chbmap_adapt_sinlat(self, icr=str()):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j/90 for i in range(360)] for j in range(89, -91, -1)])
        Z = self.cl_mpdata_sinlat

        fig = plt.figure(figsize=(8, 4))
        plt.contour(X, Y, Z, linewidths=0.7, levels=0, colors='navy')

        plt.xlabel("heliographic longitude (deg)")
        plt.ylabel("sine latitude")

        plt.xlim(0, 360)
        plt.ylim(-1, 1)

        plt.xticks(np.arange(0, 420, 60))
        plt.yticks(np.arange(-1, 1.5, 0.5))

        plt.minorticks_on()  # 刻み間隔って設定できる?

        plt.grid(which="major", color="gray", linewidth="0.3")
        plt.grid(which="minor", color="lightgray",
                 linewidth="0.2", linestyle="-")

        # plt.title(f"CR{icr} CHB map")

        print("\nif you want to finish this program, please close the figure window.")
        plt.show()

    def draw_monochbmap_adapt(self, icr=str()):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j for i in range(360)] for j in range(89, -91, -1)])
        Z = self.cl_mpdata

        # fig = plt.figure(figsize=(8,4))
        # plt.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'navy')
        #
        # plt.xlabel("carrington longitude (deg)")
        # plt.ylabel("heliographic latitude (deg)")
        #
        # plt.xlim(0, 360)
        # plt.ylim(-90, 90)
        #
        # plt.xticks(np.arange(0, 420, 60))
        # plt.yticks(np.arange(-90, 120, 30))
        #
        # plt.minorticks_on()#刻み間隔って設定できる?
        #
        # plt.grid(which="major", color="gray", linewidth="0.3")
        # plt.grid(which="minor", color="lightgray", linewidth="0.2", linestyle="-")
        # =============================
        cm = plt.cm.get_cmap("gray_r")
        # データが欠損している部分(配列には0で格納されている)はグレーで表示
        # dchbmap作成時，データ欠損箇所は999の値として保存している -> make_dchbmap_adapt.py
        # cm.set_over("0.8")
        # cm.set_under("0.8")
        fig = plt.figure(figsize=(8, 4))
        # plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12  # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in'  # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        # axを設定
        ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
        # ax.set_title(fname)
        # ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("Carrington longitude [deg]")
        ax.set_ylabel("heliographic latitude [deg]")
        ax.set_xlim([np.ndarray.min(X), np.ndarray.max(X)])
        ax.set_ylim([np.ndarray.min(Y), np.ndarray.max(Y)])
        ax.set_xticks(np.arange(0, 420, 60))
        ax.set_yticks(np.arange(-90, 120, 30))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        # print(np.ndarray.max(Z))
        # z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。
        maingraph = ax.scatter(X, Y, c=Z, vmin=0, vmax=1.2, s=35, cmap=cm)

        plt.title(f"CR{icr} CHB map")

        print("\nif you want to finish this program, please close the figure window.")
        plt.show()

    def draw_monochbmap_adapt_sinlat(self, icr=str()):
        X = np.array([[i for i in range(360)] for j in range(180)])
        Y = np.array([[j/90 for i in range(360)] for j in range(89, -91, -1)])
        Z = self.cl_mpdata_sinlat

        # fig = plt.figure(figsize=(8,4))
        # plt.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'navy')
        #
        # plt.xlabel("carrington longitude (deg)")
        # plt.ylabel("heliographic latitude (deg)")
        #
        # plt.xlim(0, 360)
        # plt.ylim(-90, 90)
        #
        # plt.xticks(np.arange(0, 420, 60))
        # plt.yticks(np.arange(-90, 120, 30))
        #
        # plt.minorticks_on()#刻み間隔って設定できる?
        #
        # plt.grid(which="major", color="gray", linewidth="0.3")
        # plt.grid(which="minor", color="lightgray", linewidth="0.2", linestyle="-")
        # =============================
        cm = plt.cm.get_cmap("gray_r")
        # データが欠損している部分(配列には0で格納されている)はグレーで表示
        # dchbmap作成時，データ欠損箇所は999の値として保存している -> make_dchbmap_adapt.py
        # cm.set_over("0.8")
        # cm.set_under("0.8")
        fig = plt.figure(figsize=(8, 4))
        # plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
        plt.rcParams['font.size'] = 12  # 適当に必要なサイズに
        plt.rcParams['xtick.direction'] = 'in'  # 目盛りをグラフ内向きに
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['axes.xmargin'] = 0.1
        plt.rcParams['axes.ymargin'] = 0.1
        # axを設定
        ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
        # ax.set_title(fname)
        # ax.grid(Falth)#グリッド線を追加
        ax.set_xlabel("Carrington longitude [deg]")
        ax.set_ylabel("heliographic latitude [deg]")
        ax.set_xlim([np.ndarray.min(X), np.ndarray.max(X)])
        ax.set_ylim([np.ndarray.min(Y), np.ndarray.max(Y)])
        ax.set_xticks(np.arange(0, 420, 60))
        plt.yticks(np.arange(-1, 1.5, 0.5))
        ax.grid(True, linewidth=0.7, alpha=0.7)

        # print(np.ndarray.max(Z))
        # z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。
        maingraph = ax.scatter(X, Y, c=Z, vmin=0, vmax=1.2, s=35, cmap=cm)

        plt.title(f"CR{icr} CHB map")

        print("\nif you want to finish this program, please close the figure window.")
        plt.show()
# ---------------------------------------------------------------------------
