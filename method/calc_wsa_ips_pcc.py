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
import icrsetting
#---------------------------------------------------------------------------
class wsa_ips_pcc:
    def __init__(self):
        self.ipsmap = [[0 for i in range(360)] for j in range(180)]
        self.wsamap = []

    def read_dat(self,fpath):
        zero_cnt =0
        low2_cnt =0
        low_cnt =0
        with open(fpath) as readfile:
            for i in range(180):
                for j in range(360):
                    #IPS_SWSのデータは南北が反転していない
                    self.ipsmap[i][j] = float(readfile.readline())
                    if self.ipsmap[i][j]==0.:
                        zero_cnt +=1
                    if self.ipsmap[i][j]>=200 and self.ipsmap[i][j]<250:
                        low2_cnt +=1
                    if self.ipsmap[i][j]>0 and self.ipsmap[i][j]<200:
                        low_cnt +=1
        print(f"zero_count(invalid): {zero_cnt}")
        print(f"low2_count(200-250): {low2_cnt}")
        print(f"low_count(0-200): {low_cnt}")

    def read_csv(self,fpath):
        with open(fpath) as readfile:
            for i in range(180):
                line = readfile.readline()
                linelist = list(line.split(","))
                linelist[-1] = linelist[-1][:(len(linelist[-1])-1)]
                list_modelv = list(map(float, linelist))
                self.wsamap.append(list_modelv)
#---------------------------------------------------------------------------
