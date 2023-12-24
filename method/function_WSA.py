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
def wsamodel(Vf,Vs,e_factor,angular_d,alpha,delta,w,k,beta=1.0,gamma=0.8):
    print(angular_d)
    print((angular_d/w)**delta)
    print(math.exp(-((angular_d/w)**delta)))
    return Vs + (Vf-Vs) * (beta-gamma*(math.exp(-((angular_d/w)**delta)))**k) / ((1+e_factor)**alpha)
#---------------------------------------------------------------------------
