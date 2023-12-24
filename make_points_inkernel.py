import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import csv
from decimal import Decimal
from scipy import signal
from tqdm import tqdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime
#---------------------------------------------------------------------------
#main
lat=90-0.5
lon=0+0.5
plist = []
poss_list = []
cnt_list = []
deg = math.pi/180

print("---------- start -------------------------------")
kernel = int(input("please a kernel number: default is 14  -->  "))#球面角度距離#全幅

for k in tqdm(range(180)):
    lat = 89.5 - k
    for i in range(180):
        for j in range(360):
            acos1 = Decimal(math.sin((89.5-i)*deg)) * Decimal(math.sin(lat*deg)) \
            + Decimal(math.cos((89.5-i)*deg)) * Decimal(math.cos(lat*deg)) \
            * Decimal(math.cos(((j+0.5)-lon)*deg))
            acos1=round(acos1, 10)
            angle = math.acos(acos1)
            if angle <= kernel/2*deg:#kernelは全幅なので半幅を使うこと
                poss_list.append([i,j])
    plist.append(poss_list)
    poss_list = []

"""
for i in range(18):
    for j in range(10):
        k = 10 * i + j
        print(len(plist[k]),end="  ")
        if j==9:
            print()
"""

for i in range(180):
    cnt_list.append(len(plist[i]))

fname=f"kernel{kernel}.txt"
with open(fname, "w") as f:
    f.write("this file includes the data that the list of the points in the specific convolution kernel\n")
    f.write(f"kernel={kernel}\n")
    for k in range(180):
        f.write(f"latitude={k}\n")
        f.write(f"count={cnt_list[k]}\n")
        for i in range(cnt_list[k]):
            f.write(f"{plist[k][i][0]}:{plist[k][i][1]}\n")
f.close()
print("----------- end --------------------------------")
