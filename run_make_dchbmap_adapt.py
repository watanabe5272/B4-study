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
import make_chbmap_adapt
import make_dchbmap
import make_dchbmap_adapt
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()

chb = make_chbmap_adapt.CH_Boundary_Adapt()
fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder="fline_adapt")
mpdata = chb.read_mpdata_adapt(fpath=fpath)

dchb_adapt = make_dchbmap_adapt.Distance_CHB_Adapt(mpdata=mpdata)
fpath = icrs.set_fpath(exts="data",bkeyword="r_s",folder="fline_adapt")
tpl, ppl = dchb_adapt.read_photoloc_adapt(fpath)

dchb = make_dchbmap.Distance_CHB(mpdata=mpdata)
dchb.theta_pl = tpl
dchb.phi_pl = ppl
dchbmap = dchb.make_dchbmap()
dchb.save_dchbmap(icr=icr, fname=f"chb{icr}_dchbmap_adapt.csv")

print("----------- end --------------------------------")
