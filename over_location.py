import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime

wrk = [[0 for i in range(360)] for j in range(180)]
theta = [[0 for i in range(360)] for j in range(180)]
phi = [[0 for i in range(360)] for j in range(180)]
d_dchb = []
d_sws = [[0 for i in range(360)] for j in range(180)]

ddir, fname = str(49), str(18)
flag1, flag2, flag3 = bool(), bool(), bool()
ddir = os.getcwd()#カレントディレクトリのパスを取得
sep = os.sep

filepath, filepath2 = str(), str()
d_dchb = []
csvname = str()
datname = str()
prex_list = []
prey_list = []
dic_lower = []
dic_higher = []
cnt_lower = 0
cnt_higher = 0

rad = math.pi/180
#vs, vf = 250., 850.

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#あらかじめ作成したcsvファイルを読み込み，d_dchb配列を返すモジュール
def read_dchbcsv(icrnx):
    #dchb_csvファイルの読み込み
    #d_dchb配列にcsvのデータが格納される
    csvname = "chb" + icrnx + "r_p_dchbmap.csv"
    print("csv file name :::", csvname)
    filepath =  ddir + sep + csvname#カレントディレクトリのパスをファイル名と結合
    flag2 = os.path.isfile(filepath)
    if flag2:
        with open(filepath) as readfile:
            for i in range(180):
                line = readfile.readline()
                lista = list(map(float, line.split(",")))
                d_dchb.append(lista)
            print()
        return d_dchb, csvname
    else:
        print("don't pick up a csv file in current directory")
        print("***** end *****")
        sys.exit()

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#あらかじめ作成したdatファイルを読み込み，d_sws配列を返すモジュール
def read_swsdat(icry):
    dic_lower = []
    dic_higher = []
    cnt_lower = 0
    cnt_higher = 0
    datname = "V"+str(icry)+"a.dat"
    print("dat file name :::", datname)
    filepath2 =  ddir + sep + datname#カレントディレクトリのパスをファイル名と結合
    flag3 = os.path.isfile(filepath2)
    if flag3:
        with open(filepath2) as readfile:
            for i in range(180):
                for j in range(360):
                    vsw = readfile.readline()
                    vsw2 = float(vsw)
                    if vsw2 < 250.:
                        dic_lower += [180-i-1, j, vsw2]
                        cnt_lower += 1
                        vsw2 = 250.
                    elif vsw2 >850.:
                        dic_higher += [180-i-1, j, vsw2]
                        cnt_higher += 1
                        csw2 = 850.
                    d_sws[180-i-1][j] = vsw2
        return d_sws, datname
    else:
        print("don't pick up a dat file in current directory")
        print("***** end *****")
        sys.exit()

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#開いた磁力線が光球上のどの座標に落ちるかを計算するモジュール
def photoloc(icrn_pl,theta_pl,phi_pl):
    theta_pl = [[0 for i in range(360)] for j in range(180)]
    phi_pl = [[0 for i in range(360)] for j in range(180)]
    flag_pl = bool()

    #ファイルの存在確認
    #あればflagがTrueになる
    fname = "flines"+str(icrn_pl)+"r_s.data"
    filepath =  ddir + sep + fname#カレントディレクトリのパスをファイル名と結合
    print("data_filepath :::", filepath)
    flag_pl = os.path.isfile(filepath)#fileの存在確認

    if flag_pl:#ファイルが存在する場合flagがTrueでこちらを実行
        print("Now reading from ",fname,"...")
        with open(filepath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(1,180):#なぜかtheta=179までなので
                for j in range(360):
                    line_s = readfile.readline()
                    line_p = readfile.readline()
                    list_s = list(map(float, line_s.split()))
                    list_p = list(map(float, line_p.split()))
                    #print(list_s)
                    #print(list_p)
                    if i != int(list_s[1]):
                        print("mismatch ( i : ",i,", thes : ",list_s[1]," )")
                    #データは南側からスキャンしているので上下逆さまに配列する
                    theta_pl[180-i-1][j] = list_p[1]
                    phi_pl[180-i-1][j] = list_p[2]
            print()
            for j in range(360):#最後1行はコピーで補う
                theta_pl[179][j] = theta_pl[178][j]
                phi_pl[179][j] = phi_pl[178][j]
        return flag_pl, fname, theta_pl, phi_pl
        #theta_pl,phi_plにはsourcesurfaceからphotosphereに落とした座標が入っている
    else:#ファイルが存在しない場合flagがFalthでプログラムは終了
        print("FILE is not found")
        print("*** end ***\n\n")
        sys.exit()

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#光球上から伸び出る磁力線が2.5Rsまで開いているかを計算するモジュール
def openarea(icrn_oa,wrk_oa):
    wrk_oa = [[0 for i in range(360)] for j in range(180)]
    flag = bool()

    #ファイルの存在確認
    #あればflagがTrueになる
    fname = "flines"+str(icrn_oa)+"r_p.data"
    filepath =  ddir + sep + fname#カレントディレクトリのパスをファイル名と結合
    print("data_filepath :::", filepath)
    flag = os.path.isfile(filepath)#fileの存在確認

    if flag:
        with open(filepath) as readfile:
            readfile.readline()
            readfile.readline()#先頭2行を読み飛ばし
            for i in range(1,180):#なぜかtheta=179までなので
                for j in range(360):
                    line_p = readfile.readline()
                    line_s = readfile.readline()
                    list_p = list(map(float, line_p.split()))
                    list_s = list(map(float, line_s.split()))
                    #print(list_p)
                    #print(list_s)
                    if list_s[0]==2.5:
                        #print("one!!!\n")
                        wrk_oa[180-i-1][j] = 1
                    else:
                        #print("zero!!!\n")
                        wrk_oa[180-i-1][j] = 0
            print()
        for j in range(360):#これは何をしている?
            wrk_oa[179][j] = wrk_oa[178][j]
        return flag, wrk_oa
    else:#ファイルが存在しない場合flagがFalthでプログラムは終了
        print("FILE is not found")
        print("*** end ***\n\n")

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#任意の点におけるCHBまでの最短距離(つまりDCHB)を計算するモジュール
def dchb(wrk_dc,phi_ph,theta_ph):
    deg = math.pi/180.0#radとdegreeの変換因子
    a_dchb = 180.0
    lonph_dchb, latph_dchb = 0, 0

    for i in range(360):#全探索して最小距離a_dchbを求める
        for j in range(180):
            if wrk_dc[j][i] == 0:
                #0~180や0~360はデータ個数的には181や361になるため，中点を取り出すことで180,360個に合わせている
                theta_x = float(j) - 89.5
                phi_x = float(i) + 0.5
                #半径1の球上での三角法
                acos1 = math.sin(theta_ph*deg) * math.sin(theta_x*deg) \
                + math.cos(theta_ph*deg) * math.cos(theta_x*deg) \
                * math.cos((phi_ph-phi_x)*deg)
                angle = math.acos(acos1)/deg

                if angle < a_dchb:
                    a_dchb = angle
                    lonph_dchb = i#バウンダリー上の最短地点
                    latph_dchb = j#バウンダリー上の最短地点
    return a_dchb, lonph_dchb, latph_dchb

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
#xにdchbの2次元配列を与えるとrileyのdchbmodelからsw速度を計算するモジュール
def dchb_model(x,epsx,wx,vfx,vsx):
    eps = epsx
    w = wx
    vf = vfx
    vs = vsx
    return vs + 0.5*( vf - vs )*( 1 + np.tanh((x-eps)/w) )

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
def pcc(x, y):
    x2, y2, = [], []
    for ii in range(180):
        for jj in range(360):
            #print(len(x), len(x[-1]))
            x2.append(x[ii][jj])
            y2.append(y[ii][jj])
    x3 = np.array(x2)
    y3 = np.array(y2)
    #print(len(x2))
    #print(len(x3))
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for ii in range(180):
        g = 0.5*(math.sin(ii*rad)+math.sin((ii+1)*rad))
        for jj in range(360):
            h = ii * 360 + jj
            sum_x += x3[h]*g
            sum_y += y3[h]*g
            sum_z += g
    #重み付き平均値を計算
    mean_x = sum_x/sum_z
    mean_y = sum_y/sum_z
    #残差を計算
    x_dif = y3 - mean_x
    y_dif = x3 - mean_y
    #残差の2乗を計算
    x_difsq = x_dif ** 2
    y_difsq = y_dif ** 2
    for ii in range(180):
        g = 0.5*(math.sin(ii*rad)+math.sin((ii+1)*rad))
        for jj in range(360):
            h = ii * 360 + jj
            x_difsq[h] *= g
            y_difsq[h] *= g
    #標準偏差を計算
    stdiv_x = np.sqrt(sum(x_difsq)/sum_z)
    stdiv_y = np.sqrt(sum(y_difsq)/sum_z)
    #共分散を計算
    sum_covar = 0
    for ii in range(180):
        g = 0.5*(math.sin(ii*rad)+math.sin((ii+1)*rad))
        for jj in range(360):
            h = ii * 360 + jj
            sum_covar += x_dif[h] * y_dif[h] * g
    covar = sum_covar/sum_z
    #重み付き相関係数PCCを計算
    pcc = covar/stdiv_y/stdiv_x

    return pcc, covar, stdiv_x, stdiv_y, mean_x, mean_y

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--

#このプログラムと同じディレクトリにデータファイルを置いておかないと実行できない
print()
print("please put a data file at current directory")
sign = input("  y or n  -->  ")
if sign == "y":#同じところに置いている
    pass
elif sign == "n":#置いていない場合終了
    print("*** end ***\n\n")
    sys.exit()
else:#入力がy,n意外の場合終了
    print("*** end ***\n\n")
    sys.exit()

print()
print("current directory :::", ddir)#カレントディレクトリの表示

icrn = input("  CRN  -->  ")#CRNの入力
print()
if len(icrn)!=4:
    print("please 4 digit")
    print("*** end ***\n\n")
    sys.exit()#CRNの入力が4桁でない場合終了

#CRNが1913と2060であればPFSSモデルとしてKPNSOを用いている
#他のCRNを調べたければKPNSOかGONGかの分岐が必要になる

d_dchb, csvname000 = read_dchbcsv(str(icrn))
d_sws, datname000 = read_swsdat(str(icrn))

#dchbrelation統計値のtxtファイル読み込んで，dchbanaly_staに格納する
dchbanaly_sta = []
filechs = glob.glob(f"mean_stdev_cr{icrn}*.txt")
print("\n-----  choose a file   -----")
for j in range(len(filechs)):
    print(f"[{j}]: {filechs[j]}")
txtnumber = int(input("\ninput a file number  -->  "))
filepath = ddir + sep + filechs[txtnumber]
#flag_crs = os.path.isfile(filepath)
with open(filepath) as readfile:
    for i in range(2):
        trush = readfile.readline()#いらない行を読み飛ばし
    #値は左からmean, variance, stndard deviation
    for i in range(350):
        line = readfile.readline()
        linelist = list(map(float, line.split(",")))
        dchbanaly_sta.append(linelist)

overlist_x = []
overlist_y = []
c=0
cc=0
for i in range(180):
    for j in range(360):
        d_deg = int(d_dchb[i][j]*rad//0.001)
        if d_deg > 50:#dchb>0.05のものはスキップ
            cc+=1
            continue
        print(d_deg)
        if dchbanaly_sta[d_deg][0]+dchbanaly_sta[d_deg][2] < d_sws[i][j]:
            overlist_y.append(i-90)
            overlist_x.append(j)
            c+=1
overarray_x = np.array(overlist_x)
overarray_y = np.array(overlist_y)
print(overarray_x)
print(overarray_y)

print()
print("Now making a figure from data...")

pre_list = []
for i in range(360):
    for j in range(180):
        xy = [i, j-90]
        pre_list.append(xy)
#print(pre_list)
prex_list = []
prey_list = []
for i in range(len(pre_list)):
    prex_list.append(pre_list[i][0])
    prey_list.append(pre_list[i][1])
x_list = np.array(prex_list)
y_list = np.array(prey_list)
#print(x_list)

z_list = []
for i in range(360):
    for j in range(180):
        z_list.append(d_sws[j][i])
#print(z_list)
#print(len(z_list))

fname = f"CR {icrn}"

cm = plt.cm.get_cmap("jet_r").copy()
cm.set_under("0.3")#データが欠損している部分(配列には0で格納されている)はグレーで表示
fig = plt.figure(figsize=(10,5))
#plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
plt.rcParams['font.size'] = 12 # 適当に必要なサイズに
plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.xmargin'] = 0.1
plt.rcParams['axes.ymargin'] = 0.1
#axを設定
ax = fig.add_axes((0.15, 0.15, 0.75, 0.7))
ax.set_title(fname)
#ax.grid(Falth)#グリッド線を追加
ax.set_xlabel("carrington longitude [deg]")
ax.set_ylabel("heliographic latitude [deg]")
ax.set_xlim([min(x_list),max(x_list)])
ax.set_ylim([min(y_list),max(y_list)])
ax.set_xticks(np.arange(0,420,60))
ax.set_yticks(np.arange(-90,120,30))
ax.grid(True, linewidth=0.7, alpha=0.7)

maingraph=ax.scatter(x_list, y_list, c=z_list, s=35, vmin=250, vmax=850, cmap=cm)#z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。

#カラーバーを追加
divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
ticks = [i for i in range(200,950,50)]
colorbar = fig.colorbar(maingraph, cax=color_ax, ticks=ticks) #新しく作成したaxesであるcolor_axを渡す

ax.scatter(overarray_x, overlist_y, s=0.05, c="red")

print(len(overlist_x), c, cc)

print()
print("if you want to finish this program, please close the figure window.")
plt.show()
