import sys
import math
import os
import numpy as np
import statistics as sta
import glob
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime as dtime
#---------------------------------------------------------------------------
class SetCrClass:
    def __init__(self):
        self.icr = str()
        self.fpath = str()

    #CRをキーボード入力から得る
    def set_icr(self):
        self.icr = input("please a number as 4 digits  -->  ")
        return self.icr

    #必要となるファイル名を作成する
    #extsは読み込むファイルの拡張子
    #拡張子が同じだが，種類の異なるファイルがあるときは，keywordに区別できるワードを設定する
    def set_fpath(self,exts,fkeyword=str(),bkeyword=str(),folder=str()):
        ddir = os.getcwd()#カレントディレクトリパスの取得
        sep = os.sep#使用しているOSにおけるセパレータの取得

        #使用したいファイルを指定する
        #--------------------------------
        #選択肢の表示
        #引数folderで指定したフォルダ内の，
        #引数extsで指定した拡張子を持つデータファイルを，選択肢として表示する
        #引数fkeyword,bkeywordを与えれば，そのキーワードの含まれるファイルのみが表示される
        filechs = glob.glob(f"{folder}/*{fkeyword}*{self.icr}*{bkeyword}*.{exts}")
        print("\n-----  choose a file   -----")
        for j in range(len(filechs)):
            print(f"[{j}]: {filechs[j]}")
        #--------------------------------
        #使用するファイルを整数値として入力し，指定する
        txtnum = int(input("\ninput a file number  -->  "))
        
        self.fpath = ddir + sep + filechs[txtnum]
        return self.fpath
#---------------------------------------------------------------------------
