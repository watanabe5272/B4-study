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
class Analyze_Scatter:
    def __init__(self,swsips,dchbmap):
        self.swsips = swsips
        self.dchbmap = dchbmap
        self.analyze = list()
        self.statisticslist = [[] for i in range(100)]
        self.increment = float()
        self.increment_horizontal = 25
        self.maxsws = float()
        self.minsws = float()
        self.statisticslist_horizontal = [[] for i in range(50)]

    def analyze_scatter(self):
        deg = math.pi/180
        num=100
        swslist = [0 for i in range(100)]
        gsumlist = [0 for i in range(100)]
        datalist = [[] for i in range(100)]
        self.increment = 0.01
        for i in range(180):
            g = math.cos((89.5-i)*deg)
            for j in range(360):
                k = int(self.dchbmap[i][j]//self.increment)
                swslist[k] += self.swsips[i][j]*g
                gsumlist[k] += g
                datalist[k].append([self.swsips[i][j],g])
        for i in range(100):
            if gsumlist[i]==0:
                num = i
                break
            swslist[i] = swslist[i]/gsumlist[i]
        swslist = swslist[:num]
        gsumlist = gsumlist[:num]
        datalist = datalist[:num]
        self.statisticslist = self.statisticslist[:num]

        difdiflist = [0 for i in range(num)]
        for i in range(num):
            for j in range(len(datalist[i])):
                difdiflist[i] += ((datalist[i][j][0]-swslist[i])**2)*datalist[i][j][1]
        for i in range(num):
            self.statisticslist[i].append(swslist[i])
            self.statisticslist[i].append(math.sqrt(difdiflist[i]/gsumlist[i]))

    def save_scatter_analysis(self,icr,fname,folder,exts,filelist,vh):
        if vh == "vertical":
            self.minsws = 0
        ddir = os.getcwd()
        sep = os.sep
        today = dtime.now()
        todaynow = today.strftime("%Y%m%d%H%M%S")
        todaynow2 = todaynow[2:]
        todaynow3 = today.strftime("%Y-%m-%d %H:%M:%S")
        fname = fname + todaynow2 + exts
        filepath = ddir + sep + folder + sep + fname
        with open(filepath,"w") as f:
            f.write(f"the result of the scatter analysis {vh}\n")
            f.write(f"{fname}\n\n")
            f.write(f"{filelist[0]}\n")
            f.write(f"{filelist[1]}\n\n")
            f.write(f"current time      : {todaynow3}\n")
            f.write(f"CR                : {icr}\n")
            f.write(f"analysis increment : {self.increment}\n\n")
            f.write("***** the result of the analysis *****\n")
            for i in range(len(self.statisticslist)):
                f.write(f"i                  : {(i+int(self.minsws//self.increment))*self.increment}\n")
                f.write(f"mean               : {self.statisticslist[i][0]}\n")
                f.write(f"standard diviation : {self.statisticslist[i][1]}\n")
        f.close()

    def analyze_scatter_horizontal(self):
        deg = math.pi/180
        num=100
        dchblist = [0 for i in range(50)]
        gsumlist = [0 for i in range(50)]
        datalist = [[] for i in range(50)]
        self.increment = 25
        self.maxsws = 0.
        self.minsws = 850.
        for i in range(180):
            for j in range(360):
                if self.maxsws < self.swsips[i][j]:
                    self.maxsws=self.swsips[i][j]
                if self.minsws > self.swsips[i][j]:
                    self.minsws=self.swsips[i][j]
        for i in range(180):
            g = math.cos((89.5-i)*deg)
            for j in range(360):
                k = int(self.swsips[i][j]//self.increment)
                dchblist[k] += self.dchbmap[i][j]*g
                gsumlist[k] += g
                datalist[k].append([self.dchbmap[i][j],g])
        #print(int(self.minsws//self.increment),int(self.maxsws//self.increment)+1)
        #print(gsumlist)
        dchblist = dchblist[int(self.minsws//self.increment) : int(self.maxsws//self.increment)+1]
        gsumlist = gsumlist[int(self.minsws//self.increment) : int(self.maxsws//self.increment)+1]
        #print(gsumlist)
        datalist = datalist[int(self.minsws//self.increment) : int(self.maxsws//self.increment)+1]
        num = len(dchblist)
        for i in range(num):
            dchblist[i] = dchblist[i]/gsumlist[i]

        self.statisticslist = [[] for i in range(num)]
        difdiflist = [0 for i in range(num)]
        for i in range(num):
            for j in range(len(datalist[i])):
                difdiflist[i] += ((datalist[i][j][0]-dchblist[i])**2)*datalist[i][j][1]
        for i in range(num):
            self.statisticslist[i].append(dchblist[i])
            self.statisticslist[i].append(math.sqrt(difdiflist[i]/gsumlist[i]))
#---------------------------------------------------------------------------
