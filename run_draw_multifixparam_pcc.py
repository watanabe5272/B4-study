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
swsips, dchbmap = [], []

pcc = fitting_maxpcc.Fitting_MaxPCC(swsips=swsips, dchbmap=dchbmap)
#pcc.set_increment()
numbers = input("input some numbers of CR (segment : ,)  -->  ")
numbers = list(map(str, numbers.split(",")))
fixparam = input("which do you fix, eps or w  -->  ")
if fixparam=="eps":
    pcc.sign_param=0
elif fixparam=="w":
    pcc.sign_param=1
for x in numbers:
    icrs.icr=x
    fpath = icrs.set_fpath(exts="txt",bkeyword=f"{fixparam}",folder="result_fix_param")
    pcc.read_fixingtxt(fpath=fpath)
pcc.draw_multi_fixingresult(list_title=numbers)

print("----------- end --------------------------------")
