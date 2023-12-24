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
import draw_scatterplot
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()#クラス
icr = icrs.set_icr()
# fpath = icrs.set_fpath(exts="csv",fkeyword="dchbmap",folder="convdchbmap_adapt_csv")

# draw = draw_dchbmap.Draw_DCHBmap()#クラス
# dchbmap = draw.read_csv(fpath=fpath,adapt=1)

ips = make_swsmap.SWS()#クラス
fpath = icrs.set_fpath(exts="dat",fkeyword="V",folder="ips_vdat")
swsips = ips.read_dat(fpath=fpath)

scatter = draw_scatterplot.Draw_Scatterplot()#クラス
# scatter.set_dchbmap(dchbmap=dchbmap)
scatter.set_swsips(swsips=swsips)
# fpath = icrs.set_fpath(exts="txt",fkeyword="fitting",folder="fitting_result")
# scatter.read_fittingresult_txt(fpath=fpath)
# fpath = icrs.set_fpath(exts="txt",fkeyword="scatter",bkeyword="vert",folder="scatter_analysis_adapt")
# scatter.read_scatteranalysis_txt(fpath=fpath)
# fpath = icrs.set_fpath(exts="txt",fkeyword="scatter",bkeyword="hori",folder="scatter_analysis_adapt")
# scatter.read_scatteranalysis_txt_hori(fpath=fpath)
fpath = icrs.set_fpath(exts="csv",fkeyword="modelv",folder="modelv_adapt")
scatter.read_csv_adapt(fpath=fpath)

fpath = icrs.set_fpath(exts="txt",fkeyword="fitting",folder="fitting_result")
scatter.read_fittingresult_txt(fpath)
scatter.single_regression()#単回帰直線の傾きと切片の決定

scatter.draw_scatterplot_linear(icr=icr,fname=f"")

print("----------- end --------------------------------")
