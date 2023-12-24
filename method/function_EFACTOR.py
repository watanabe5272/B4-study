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
def expansion_factor(photomag,sourcemag,photo=1.0,source=2.5):
    return ((photo/source)**2) * abs((photomag/sourcemag))
#---------------------------------------------------------------------------
