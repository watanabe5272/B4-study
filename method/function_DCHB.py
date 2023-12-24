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
def dchbmodel(Vf,Vs,angular_d,eps,w):
    return Vs + (1/2)*(Vf-Vs)*(1+np.tanh((angular_d-eps)/w))

def dchbmodel_array(Vf,Vs,array_d,eps,w):
    culc_sws = array_d
    for i in range(len(array_d)):
        culc_sws[i] = Vs + (1/2)*(Vf-Vs)*(1+math.tanh((array_d[i]-eps)/w))
    return culc_sws
#---------------------------------------------------------------------------
