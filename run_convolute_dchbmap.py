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
import draw_dchbmap
import convolute_dchbmap
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()
fpath = icrs.set_fpath(exts="csv",bkeyword="dchbmap",folder="dchbmap_csv")
draw = draw_dchbmap.Draw_DCHBmap()
dchbmap = draw.read_csv(fpath=fpath,adapt=0)
conv = convolute_dchbmap.Convo_Gauss_2D(dchbmap=dchbmap)
conv_dchbmap = conv.convolution(oddangle=15)

draw.dchbmap = conv_dchbmap
draw.rad_to_deg()
draw.draw_dchbmap(icr=icr)
print("----------- end --------------------------------")
