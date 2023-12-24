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
import astropy.units as u
import astropy.io.fits as fits
import sunpy.visualization.colormaps as cm
#---------------------------------------------------------------------------
#実行ファイルのあるディレクトリ内のデータフォルダを検索範囲に追加する
ddir = os.getcwd()
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))
#自作のメソッドファイルを読み込む
import icrsetting
import draw_dchbmap
import make_modelvmap
import make_chbmap_adapt
import draw_scatterplot
import function_WSA as fWSA
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

# ==========================================================================
icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()
chb = make_chbmap_adapt.CH_Boundary_Adapt()
fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder="fline_adapt")
chbmap = chb.read_mpdata_adapt(fpath=fpath)
chb.toSineLatitude()

# ==========================================================================

hdulist=fits.open('EUVfits/EIT195_sin_synop_CR'+ icr +'.fits')
hdu=hdulist[0]
data=hdu.data
header=hdu.header
# for x in header:
#     print(x)
# print(data.shape)
data_rev = np.flipud(data).copy()
data_resize = [[0 for _ in range(360)] for _ in range(180)]
for i in range(180):
    for j in range(360):
        unit_sum = 0
        for k in range(8):
            for l in range(10):
                unit_sum += data_rev[i*8+k][j*10+l]
        data_resize[i][j] = unit_sum / 80
data_resize = np.array(data_resize)

# EIT195 colormap import
c = cm.color_tables.eit_color_table(195*u.angstrom)

X = np.array([[i for i in range(360)] for j in range(180)])
Y = np.array([[j/90 for i in range(360)] for j in range(89,-91,-1)])
# Y = np.array([[j for i in range(360)] for j in range(89,-91,-1)])
Z = list()
for i in range(180):
    for j in range(360):
        Z.append(data_resize[i][j])
Z = np.array(Z)

cm = c # EIT195 colormap
# cm.set_over("0.7")
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
ax.set_ylabel("sine latitude")
ax.set_xlim([np.ndarray.min(X),np.ndarray.max(X)])
ax.set_ylim([np.ndarray.min(Y),np.ndarray.max(Y)])
ax.set_xticks(np.arange(0,420,60))
ax.set_yticks(np.arange(-1.0,1.5,0.5))
ax.grid(True, linewidth=0.7, alpha=0.7)
# maingraph=ax.scatter(X, Y, c=Z, vmin=np.min(Z), vmax=np.max(Z), s=35, cmap=cm)
maingraph=ax.scatter(X, Y, c=Z, cmap=cm)
# z_listの最小値と最大値をカラースケールの最大値、最小値として用いる。

# ============================================================================
# icrs = icrsetting.SetCrClass()
# icr = icrs.set_icr()
# chb = make_chbmap_adapt.CH_Boundary_Adapt()
# fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder="fline_adapt")
# chbmap = chb.read_mpdata_adapt(fpath=fpath)
# chb.toSineLatitude()

Z = chb.cl_mpdata_sinlat
ax.contour(X, Y, Z, linewidths = 0.7, levels = 0, colors = 'orange')
#カラーバーを追加
divider = make_axes_locatable(ax) #グラフaxの外枠に仕切り(AxesDivider)を作成
color_ax = divider.append_axes("right", size="1%", pad="5%") #append_axesで新しいaxesを作成
ticks = [i for i in range(-50,1000,900)]
colorbar=fig.colorbar(maingraph, cax=color_ax,ticks=ticks) #新しく作成したaxesであるcolor_axを渡す。
# colorbar=fig.colorbar(maingraph, cax=color_ax)
print("\nif you want to finish this program, please close the figure window.")
plt.show()

# plt.imshow(data_resize, cmap=c)
# plt.show()

print("----------- end --------------------------------")
