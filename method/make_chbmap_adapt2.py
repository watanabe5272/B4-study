import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import csv
from decimal import Decimal, ROUND_HALF_UP
from scipy import signal
from tqdm import tqdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime
#---------------------------------------------------------------------------
class CH_Boundary_Adapt2:
    def __init__(self):
        self.mpdata = [[0 for i in range(360)] for j in range(180)]

    #KPVTもしくはGONGの磁場データを読みこんでopen/closeを判定した結果を戻り値とする
    #ADAPTをこのメソッドで読みこむ
    #ADAPTというか，途中計算が入っているデータを読み込む用
    #ncountを読み込んで，途中計算を読み飛ばすことができる
    #KPVTのデータには途中計算がなく，1.0と2.5のデータ(計算結果)のみが入っている
    def read_mpdata_adapt2(self,fpath):
        with open(fpath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(179):#磁場データは179行分しかない
                for j in range(360):
                    readfile.readline()#theta, phiの情報を1行分読み飛ばす
                    #計算回数ncoutを読み取る---------------------------------
                    countline = readfile.readline()
                    countlist = list(countline.split("="))
                    countnum = int(countlist[1])#ncount
                    #-----------------------------------------------------
                    line_s = readfile.readline()#SourceSurface#初期位置
                    for k in range(countnum-1):#途中計算は読み飛ばす
                        readfile.readline()
                    line_p = readfile.readline()#photosphere#最終位置
                    list_s = list(map(float, line_s.split()))#初期位置のデータをリスト化
                    list_p = list(map(float, line_p.split()))#最終位置のデータをリスト化
                    #-----------------------------------------------------
                    thetax = round(list_p[1])#最終位置の緯度シータを四捨五入する
                    if thetax == 180:#緯度180度は折り返して緯度0度とする
                        thetax = 0
                    phix = round(list_p[2])#最終位置の経度ファイを四捨五入する
                    if phix == 360:#経度360度は折り返して経度0度とする
                        phix = 0
                    #SourceSurfaceからおろしてきた磁力線(開いた磁力線)が
                    #Photosphereにて到達・接続した位置は1とする
                    #そのような磁力線が接続していないPhotosphereの位置は0が入っている
                    self.mpdata[thetax][phix]=1
                    #-----------------------------------------------------
            #用意したリストは180行だが，データは179行分しかない
            #こちらで179行目をコピーして180行目を補う
            #リストのインデックスとしては178,179に対応しているのは言うまでもない
            for j in range(360):
                self.mpdata[179][j] = self.mpdata[178][j]
            #print(self.mpdata[-2])
        return self.mpdata
#---------------------------------------------------------------------------
