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
import analyze_scatter_adapt
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

analy = analyze_scatter_adapt.Analyze_Scatter(swsips=swsips,dchbmap=dchbmap)
analy.analyze_scatter()
analy.save_scatter_analysis(icr=icr,fname=f"scatter_analysis{icr}_adapt_vertical",folder="scatter_analysis_adapt",exts=".txt",filelist=filelist,vh="vertical")
analy.analyze_scatter_horizontal()
analy.save_scatter_analysis(icr=icr,fname=f"scatter_analysis{icr}_adapt_horizontal",folder="scatter_analysis_adapt",exts=".txt",filelist=filelist,vh="horizontal")
print("----------- end --------------------------------")
