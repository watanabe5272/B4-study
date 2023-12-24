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
import draw_dchbmap
import make_dchbmap_adapt
import draw_dchbmap_onphoto
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()

chb = make_chbmap_adapt.CH_Boundary_Adapt()
fpath = icrs.set_fpath(exts="data",bkeyword="r_p",folder="fline_adapt")
chbmap = chb.read_mpdata_adapt(fpath=fpath)

dchb_adapt = make_dchbmap_adapt.Distance_CHB_Adapt(mpdata=chbmap)
fpath = icrs.set_fpath(exts="data",bkeyword="r_s",folder="fline_adapt")
theta, phi = dchb_adapt.read_photoloc_adapt(fpath)

draw = draw_dchbmap.Draw_DCHBmap()
#fpath = icrs.set_fpath(exts="csv",bkeyword="conv",folder="convdchbmap_adapt_csv")
fpath = icrs.set_fpath(exts="csv",bkeyword="dchbmap_adapt",folder="dchbmap_adapt_csv")
dchbmap = draw.read_csv(fpath=fpath,adapt=1)
draw.rad_to_deg()
dchbmap = draw.dchbmap

onphoto = draw_dchbmap_onphoto.Draw_DCHBmap_onPhoto(chbmap=chbmap,\
dchbmap=dchbmap,theta=theta,phi=phi)
onphoto.make_dchbmap_onphoto()
onphoto.draw_dchbmap_onphoto(icr=icr,fname="figure title")

print("----------- end --------------------------------")
