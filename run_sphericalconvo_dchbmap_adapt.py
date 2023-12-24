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
#実行ファイルのあるディレクトリ内のデータフォルダを検索範囲に追加する
ddir = os.getcwd()
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))
#自作のメソッドファイルを読み込む
import icrsetting
import make_dchbmap
import draw_dchbmap
import sphericalconvo_dchbmap
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()#クラス
icr = icrs.set_icr()
fpath = icrs.set_fpath(exts="csv",bkeyword="dchbmap",folder="dchbmap_adapt_csv")
draw = draw_dchbmap.Draw_DCHBmap()#クラス
dchbmap = draw.read_csv(fpath=fpath,adapt=1)
conv = sphericalconvo_dchbmap.SphericalConvo_Gauss_2D(dchbmap=dchbmap)#クラス
icrs.icr = str()#kernelのファイル名にはicrが含まれない
fpath = icrs.set_fpath(exts="txt",folder="kernel")
conv.read_kernel_txt(fpath=fpath)
conv_dchbmap = conv.spherical_convolution()
#conv.save_convdchbmap(icr=icr)

draw.dchbmap = conv.conv_dchbmap
#print(draw.dchbmap[-1][0:5])
draw.rad_to_deg()
draw.draw_dchbmap(icr=icr)

conv.save_convdchbmap(icr=icr,fname=f"dchbmap{icr}_conv",folder="convdchbmap_adapt_csv",exts=".csv")
print("----------- end --------------------------------")
