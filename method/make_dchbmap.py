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
class Distance_CHB:
    def __init__(self,mpdata):
        self.mpdata = mpdata
        self.theta_pl = [[0 for i in range(360)] for j in range(360)]
        self.phi_pl = [[0 for i in range(360)] for j in range(360)]
        self.dchbmap = list()
        self.fname = str()

    #2.5Rsの磁力線のフットポイントの緯度をtheta_plとして，経度をphi_plとして返す
    def read_photoloc(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(179):#磁場データは179行分しかない
                for j in range(360):
                    line_s = readfile.readline()
                    line_p = readfile.readline()
                    list_s = list(map(float, line_s.split()))
                    list_p = list(map(float, line_p.split()))
                    self.theta_pl[i][j] = list_p[1]
                    self.phi_pl[i][j] = list_p[2]
            for j in range(360):##1行分はこちらで補う
                self.theta_pl[179][j] = self.theta_pl[178][j]
                self.phi_pl[179][j] = self.phi_pl[178][j]
        return self.theta_pl, self.phi_pl

    #open磁場内のある1地点におけるCHBまでの最小角度距離を全探索で計算
    def calc_dchb(self,theta_ph,phi_ph):
        deg = math.pi/180.
        min_dist = float(180.)
        lat_p, lon_p = int(0), int(0)

        t_ph = theta_ph
        p_ph = phi_ph

        for i in range(180):
            for j in range(360):
                if self.mpdata[i][j]==1:
                    continue
                elif self.mpdata[i][j]==0:
                    theta_x = 89.5 - float(i)
                    phi_x = float(j) + 0.5

                    acos1 = math.sin(t_ph*deg) * math.sin(theta_x*deg) \
                    + math.cos(t_ph*deg) * math.cos(theta_x*deg) \
                    * math.cos((p_ph-phi_x)*deg)

                    angle = math.acos(acos1)

                    if angle < min_dist:
                        min_dist = angle
                        lat_p = i#バウンダリー上の最短地点の緯度(0-179)
                        lon_p = j#バウンダリー上の最短地点の経度(0-359)
        return min_dist, lat_p, lon_p

    #dchbリストをradで用意しているので，degに変換する
    def rad_to_deg(self,list_ch):
        rad = 180./math.pi
        list_after = list()
        for i in range(180):
            list_after.append(list())
            for j in range(360):
                x = list_ch[i][j]*rad
                list_after[i].append(x)
        return list_after

    #openな磁場を持つ全座標において，calc_dchbを実行してdchbmapを作成する
    def make_dchbmap(self):
        print("it takes about 60 minutes to calculate dchbmap. run this program?")
        if input("  y or n  -->  ")!="y":
            sys.exit()

        for k in tqdm(range(180)):
            self.dchbmap.append(list())
            for l in tqdm(range(360), leave=False):
                if self.theta_pl[k][l]== -1e8 and self.phi_pl[k][l]== -1e8:
                    self.dchbmap[k].append(-1e8)
                    continue
                else:
                    m,lat,lon = self.calc_dchb(theta_ph=90-self.theta_pl[k][l],phi_ph=self.phi_pl[k][l])
                    self.dchbmap[k].append(float(format(m, ".4f")))
                    continue
        return self.dchbmap

    #作成したdchbmapをcsvファイルとして保存する
    def save_dchbmap(self,icr,fname):
        self.fname = fname
        for i in range(180):
            self.dchbmap[i] = list(map(str, self.dchbmap[i]))
        with open(fname, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.dchbmap)
        f.close()
#---------------------------------------------------------------------------
