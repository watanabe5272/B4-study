import sys
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import csv

wrk = [[0 for i in range(360)] for j in range(180)]
theta = [[0 for i in range(360)] for j in range(180)]
phi = [[0 for i in range(360)] for j in range(180)]

ddir, fname = str(49), str(18)
flag1, flag2 = bool(), bool()#今は使用していないが，検索したファイルが存在したらflagを付ける
ddir = os.getcwd()#カレントディレクトリのパスを取得
sep = os.sep

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--
def photoloc(icrn_pl,theta_pl,phi_pl):
    theta_pl = [[0 for i in range(360)] for j in range(180)]
    phi_pl = [[0 for i in range(360)] for j in range(180)]
    flag = bool()

    #ファイルの存在確認
    #あればflagがTrueになる
    fname = "flines"+str(icrn_pl)+"r_s.data"
    filepath =  ddir + sep + fname#カレントディレクトリのパスをファイル名と結合
    print("data_filepath :::", filepath)
    flag = os.path.isfile(filepath)#fileの存在確認

    if flag:#ファイルが存在する場合flagがTrueでこちらを実行
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
                    print(list_s)
                    print(list_p)
                    if i != int(list_s[1]):
                        print("mismatch ( i : ",i,", thes : ",list_s[1]," )")
                    #データは南側からスキャンしているので上下逆さまに配列する
                    theta_pl[180-i-1][j] = list_p[1]
                    phi_pl[180-i-1][j] = list_p[2]
            print()
            for j in range(360):#最後1行はコピーで補う
                theta_pl[179][j] = theta_pl[178][j]
                phi_pl[179][j] = phi_pl[178][j]
        return flag, fname, theta_pl, phi_pl
        #theta,phiにはsourcesurfaceからphotosphereに落とした座標が入っている
    else:#ファイルが存在しない場合flagがFalthでプログラムは終了
        print("FILE is not found")
        print("*** end ***\n\n")

#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--

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
                    print(list_p)
                    print(list_s)
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

def dchb(wrk_dc,phi_ph,theta_ph):
    pai = 3.1415926535
    deg = pai/180.0#radとdegreeの変換因子
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
print()
print("in this program, you are using KPNSO as PFSS model")

flag1, fname, theta, phi = photoloc(icrn_pl=icrn, theta_pl=theta, phi_pl=phi)

flag2, wrk = openarea(icrn_oa=icrn, wrk_oa=wrk)

lonss, latss = map(int, \
input(" input Source Surface Lon(1:360) and Lat(-90:89)  -->  ").split())

print("Longitude on Photosphere (deg) : ",phi[latss+90][lonss-1])
print("Latitude on Photosphere (deg) : ",90.0-theta[latss+90][lonss-1])

#figure出力
print()
print("csv file was not made")
print()
print("Now making a figure from data...")
x = [[i for i in range(360)] for j in range(180)]
y = [[j for i in range(360)] for j in range(-90,90)]
X = np.array(x)
Y = np.array(y)
Z = np.array(wrk)

fig = plt.figure(figsize=(9,5))
#boundaryを描画
plt.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'navy')

#source_surface の open_line が光球面のどこに落ちたかをバツマークでプロット
label_ph = "["+str(phi[latss+90][lonss-1])+", "+str(90.0-theta[latss+90][lonss-1])+"]"
plt.plot(phi[latss+90][lonss-1], 90.0-theta[latss+90][lonss-1], marker="x", markersize=7, color="g", label=label_ph)

a_dchb, lonph_dchb, latph_dchb = dchb(wrk_dc=wrk, phi_ph=phi[latss+90][lonss-1], \
theta_ph=90-theta[latss+90][lonss-1])
#a_dchbは単位degreeである。

print("lonph_dchb : ",lonph_dchb, ", latph_dchb :",latph_dchb, ", a_dchb :",a_dchb)

#バウンダリー上の最短地点を三角マークでプロット
label_dchb = "["+str(lonph_dchb)+", "+str(latph_dchb)+"]"
plt.plot(float(lonph_dchb)-0.5,float(latph_dchb-90)-0.5, marker="^", markersize=6, color="r", fillstyle="none", label=label_dchb)

plt.xlabel("carrington longitude (deg)")
plt.ylabel("heliographic latitude (deg)")

plt.xlim(0, 360)
plt.ylim(-90, 90)

plt.xticks(np.arange(0, 420, 60))
plt.yticks(np.arange(-90, 120, 30))

plt.minorticks_on()#刻み間隔って設定できる?

plt.grid(which="major", color="gray", linewidth="0.3")
plt.grid(which="minor", color="lightgray", linewidth="0.2", linestyle="-")

plt.title(fname)

plt.legend(loc="lower right", fontsize=5, ncol=1)

print()
print("if you want to finish this program, please close the figure window.")
plt.show()
