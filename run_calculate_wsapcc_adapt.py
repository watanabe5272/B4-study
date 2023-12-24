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
import calc_wsa_ips_pcc
import function_PCC as fpcc
#---------------------------------------------------------------------------
#main
print("---------- start -------------------------------")

icrs = icrsetting.SetCrClass()#クラス
cwip = calc_wsa_ips_pcc.wsa_ips_pcc()#クラス

icr = icrs.set_icr()

fpath = icrs.set_fpath(exts="csv",fkeyword="wsamap",folder="wsamodelv_adapt")
cwip.read_csv(fpath=fpath)

fpath = icrs.set_fpath(exts="dat",fkeyword="V",folder="ips_vdat")
cwip.read_dat(fpath=fpath)

ResultListPCC = list(fpcc.weighted_PCC(x=cwip.wsamap,y=cwip.ipsmap))

print()
print(f"   mean X        :  {ResultListPCC[0]}")
print(f"   mean Y        :  {ResultListPCC[1]}")
print(f"   stdiv X       :  {ResultListPCC[2]}")
print(f"   stdiv Y       :  {ResultListPCC[3]}")
print(f"   covariance    :  {ResultListPCC[4]}")
print(f"   weighted PCC  :  {ResultListPCC[5]}")
print()

print("----------- end --------------------------------")
