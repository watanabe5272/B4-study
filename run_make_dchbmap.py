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
import make_dchbmap
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()

chb = make_chbmap.CH_Boundary()
folder = input("rev, rev2, gong?  -->  ")
fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder="fline_"+folder)
mpdata = chb.read_mpdata(fpath=fpath)

dchb = make_dchbmap.Distance_CHB(mpdata=mpdata)
fpath = icrs.set_fpath(exts="data",bkeyword="r_s",folder="fline_"+folder)
tpl, ppl = dchb.read_photoloc(fpath)
dchbmap = dchb.make_dchbmap()
dchb.save_dchbmap(icr=icr, fname=f"chb{icr}_dchbmap_{folder}.csv")

print("----------- end --------------------------------")
