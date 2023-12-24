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
import function_RMSEandMEANBIAS as fRM
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()#クラス
icr = icrs.set_icr()

ips = make_swsmap.SWS()#クラス
fpath = icrs.set_fpath(exts="dat",fkeyword="V",folder="ips_vdat")
swsips = ips.read_dat(fpath=fpath)

scatter = draw_scatterplot.Draw_Scatterplot()#クラス
scatter.set_swsips(swsips=swsips)

fpath = icrs.set_fpath(exts="csv",fkeyword="modelv",folder="modelv_adapt")
scatter.read_csv_adapt(fpath=fpath)

modelv = scatter.modelv

rmse,normrmse,mbias = fRM.RMSEandMEANBIAS(f_model=modelv, y_obs=swsips)
print(rmse,normrmse,mbias)


print("----------- end --------------------------------")
