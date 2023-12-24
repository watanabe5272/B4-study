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
import astropy.io.fits as fits
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
import draw_scatterplot
import function_WSA as fWSA
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()

fpath = icrs.set_fpath(exts="csv",fkeyword="dchbmap",folder="convdchbmap_adapt_csv")
draw = draw_dchbmap.Draw_DCHBmap()
dchbmap = draw.read_csv_adapt(fpath=fpath)

fpath = icrs.set_fpath(exts="csv",fkeyword="efactormap",folder="convefactormap_adapt")
#fpath = icrs.set_fpath(exts="csv",fkeyword="efactormap",folder="expansionfactor")
efactormap = draw.read_csv_adapt(fpath=fpath)

modelv = make_modelvmap.Make_Modelvmap(dchbmap=dchbmap,eps=0,w=0)
modelv.set_efactormap(efactormap=efactormap)
#print(modelv.efactormap[0][0])
modelv.make_wsamap()
#print(modelv.modelvmap[0][-5:-1])

modelv.round_speed()

modelv.draw_modelvmap(icr=icr,fname="")
modelv.save_modelvmap(icr=icr,fname=f"wsamap{icr}_adapt",folder="wsamodelv_adapt",exts=".csv")

print("----------- end --------------------------------")
