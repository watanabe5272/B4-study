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
import function_WSA as fWSA
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

d = 0.4
f = 10
modelv = make_modelvmap.Make_Modelvmap(dchbmap=[],eps=0,w=0)
for i in range(1000,10001,1000):
    f = i
    print(f"\n{i}\t:  ",end="")
    print(fWSA.wsamodel(Vf=modelv.EUHFORIA["Vf"],Vs=modelv.EUHFORIA["Vs"],e_factor=f,angular_d=d,alpha=modelv.EUHFORIA["alpha"],delta=modelv.EUHFORIA["delta"],w=modelv.EUHFORIA["w"],k=modelv.EUHFORIA["k"],beta=modelv.EUHFORIA["beta"],gamma=modelv.EUHFORIA["gamma"]))

print("----------- end --------------------------------")
