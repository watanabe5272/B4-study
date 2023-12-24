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
import make_modelvmap
import draw_scatterplot
import function_DCHB as fDCHB
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()

fpath = icrs.set_fpath(exts="csv",bkeyword="dchbmap",folder="dchbmap_csv")
draw = draw_dchbmap.Draw_DCHBmap()
dchbmap = draw.read_csv_adapt(fpath=fpath)

swsips = []
scatter = draw_scatterplot.Draw_Scatterplot(swsips=swsips, dchbmap=dchbmap)#クラス
fpath = icrs.set_fpath(exts="txt",fkeyword="fitting",folder="fitting_result")
statics, parameter = scatter.read_fittingresult_txt(fpath=fpath)
print(parameter)
modelv = make_modelvmap.Make_Modelvmap(dchbmap=dchbmap,eps=parameter[0],w=parameter[1])
modelv.make_modelvmap()
modelv.draw_modelvmap(icr=icr,fname="figure title")

print("----------- end --------------------------------")
