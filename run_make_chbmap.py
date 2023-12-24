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
import make_chbmap
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()
folder = "fline_"+input("input the flines file : rev, rev2, gong  -->  ")
fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder=folder)

chb2 = make_chbmap.CH_Boundary()
mpdata = chb2.read_mpdata(fpath=fpath)
chb2.draw_chbmap(icr=icr)

print("----------- end --------------------------------")
