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
import make_swsmap
import fitting_maxpcc
import function_DCHB as fDCHB
import function_PCC as fpcc
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")
filelist = [0,0]

icrs = icrsetting.SetCrClass()#クラス
icr = icrs.set_icr()
fpath = icrs.set_fpath(exts="csv",fkeyword="dchbmap",folder="convdchbmap_adapt_csv")
filelist[0] = fpath
draw = draw_dchbmap.Draw_DCHBmap()#クラス
dchbmap = draw.read_csv(fpath=fpath,adapt=1)

ips = make_swsmap.SWS()#クラス
fpath = icrs.set_fpath(exts="dat",fkeyword="V",folder="ips_vdat")
filelist[1] = fpath
swsips = ips.read_dat(fpath=fpath)

pcc = fitting_maxpcc.Fitting_MaxPCC(swsips=swsips, dchbmap=dchbmap)
#pcc.set_increment()
pcc.transition_pcc()
pcc.save_fixingresult(icr=icr,fname=f"fixparam{icr}_adapt",folder="result_fix_param",exts=".txt")
pcc.draw_fixingresult()

print("----------- end --------------------------------")
