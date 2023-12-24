import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime
#---------------------------------------------------------------------------
#実行ファイルのあるディレクトリ内のデータフォルダを検索範囲に追加する
ddir = os.getcwd()
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))

import function_DCHB as fDCHB
import draw_scatterplot
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

ans = int(input("which parameters do you know about?  [0]: default  [1]:epsilon  [2]:w  -->  "))
fname = input("graph title (if you needn't the one, press enter key)   ->  ")

# X = np.array(self.dchbmap)
# Y = np.array(self.swsips)

#cm = plt.cm.get_cmap("jet_r")
fig = plt.figure(figsize=(10,7))
#plt.rcParams['font.family'] = 'Times New Roman'#フォントがなければダウンロードの必要あり。
plt.rcParams['font.size'] = 16 # 適当に必要なサイズに
plt.rcParams['xtick.direction'] = 'in' # 目盛りをグラフ内向きに
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.xmargin'] = 0.1
plt.rcParams['axes.ymargin'] = 0.1
plt.rcParams['legend.fontsize'] = 20
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.rcParams['label.fontsize'] = 16
#axを設定
ax = fig.add_axes((0.1, 0.1, 0.85, 0.8))
ax.set_title(fname)
#ax.grid(Falth)#グリッド線を追加
ax.set_xlabel("distance to coronal hole boundary [rad]")
ax.set_ylabel("solar wind speed [km/s]")
ax.set_xlim([0,0.45])
ax.set_ylim([150,900])
ax.set_xticks(np.arange(0,0.50,0.05),fontsize=10)
ax.set_yticks(np.arange(150,950,50))
ax.grid(True, linewidth=0.7, alpha=0.7)

eps = 0.1
w   = 0.1
number = 6

p = np.linspace(0,1,360*5)
#print("**************", self.list_parameter)
if ans == 0:
    cm = plt.get_cmap("Reds")
    epsi = 0.05
    wi = 0.05
    ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=epsi,w=wi), color=cm(0.75), label=f"epsilon={epsi}, w={wi}")
    ax.legend(loc='lower right')

elif ans == 1:
    cm = plt.get_cmap("Reds")
    for i in  range(1,number):
        z = i / number
        epsi = eps * z
        wi = 0.05
        ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=epsi,w=wi), color=cm((1+3*z)/4), label=f"eps={epsi:.3}, w={wi:.3}")
    ax.legend(loc='lower right')

elif ans == 2:
    cm = plt.get_cmap("Blues")
    for i in  range(1,number):
        z = i / number
        wi = w * z
        epsi = 0.05
        ax.plot(p, fDCHB.dchbmodel(Vf=850,Vs=200,angular_d=p,eps=epsi,w=wi), color=cm((1+3*z)/4), label=f"eps={epsi:.3}, w={wi:.3}")
    ax.legend(loc='lower right')

print()
print("if you want to continue to next work, please close the figure window.")
plt.show()

print("----------- end --------------------------------")
