import numpy as np
from main import *
from PIL import Image
import os
class Mean_Std(QtCore.QThread):
    update_data = QtCore.pyqtSignal(list)
    process_bar = QtCore.pyqtSignal(int)
    def __init__(self,filename):
        super(Mean_Std,self).__init__()
        self.filename = filename
        self.Mean = [0,0,0]
        self.Std = [0,0,0]
    def run(self):
        i = 0
        result = []
        Means_R = []
        Means_G = []
        Means_B = []
        Stds_R = []
        Stds_G = []
        Stds_B = []
        for item in self.filename:
            img = Image.open(item)
            img = np.array(img)
            img_R = img[:,:,0]/255
            img_G = img[:,:,1]/255
            img_B = img[:,:,2]/255
            img_R_mean = np.mean(img_R)
            img_G_mean = np.mean(img_G)
            img_B_mean = np.mean(img_B)
            img_R_std = np.std(img_R)
            img_G_std = np.std(img_G)
            img_B_std = np.std(img_B)
            Means_R.append(img_R_mean)
            Means_G.append(img_G_mean)
            Means_B.append(img_B_mean)
            Stds_R.append(img_R_std)
            Stds_G.append(img_G_std)
            Stds_B.append(img_B_std)
            i+=1
            self.process_bar.emit(i)
        a = [Means_R, Means_G, Means_B]
        b = [Stds_R, Stds_G, Stds_B]
        self.Mean[0] = np.mean(a[0])
        self.Mean[1] = np.mean(a[1])
        self.Mean[2] = np.mean(a[2])
        self.Std[0] = np.std(b[0])
        self.Std[1] = np.std(b[1])
        self.Std[2] = np.std(b[2])
        result.append(self.Mean)
        result.append(self.Std)
        self.update_data.emit(result)
