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
# ---------------------------------------------------------------------------
# 実行ファイルのあるディレクトリ内のデータフォルダを検索範囲に追加する
ddir = os.getcwd()
files = os.listdir(ddir)
files_dir = [f for f in files if os.path.isdir(os.path.join(ddir, f))]
for x in files_dir:
    sys.path.append(os.path.join(x))

# 自作のメソッドファイルを読み込む
import make_chbmap_adapt2
import make_chbmap_adapt
import icrsetting
# ---------------------------------------------------------------------------
# main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()
icr = icrs.set_icr()
fpath = icrs.set_fpath(exts="data", bkeyword="r_s", folder="fline_adapt")

chb2 = make_chbmap_adapt2.CH_Boundary_Adapt2()
mpdata = chb2.read_mpdata_adapt2(fpath=fpath)
chb = make_chbmap_adapt.CH_Boundary_Adapt()
chb.cl_mpdata = np.array(mpdata)

# ============= sine latitude モジュールのテスト ==================
# test_mpdata = [[0 for _ in range(360)] for _ in range(180)]
# for i in range(180):
#     for j in range(360):
#         if i < (179-round(j/2)):
#             test_mpdata[i][j] = 1
# chb.cl_mpdata = np.array(test_mpdata)
# chb.toSineLatitude()

# test_mpdataをそのままみたいなら下のコメントアウトを外す
# chb.cl_mpdata_sinlat = chb.cl_mpdata

# chb.draw_chbmap_adapt_sinlat(icr=icr)
# ==============================================================

chb.toSineLatitude()
chb.draw_chbmap_adapt_sinlat(icr=icr)
chb.draw_monochbmap_adapt_sinlat(icr=icr)

print("----------- end --------------------------------")
