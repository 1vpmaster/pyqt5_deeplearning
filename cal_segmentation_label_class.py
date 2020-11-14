import os
import collections
import cv2

dir_list = os.listdir("data")
dict_class = collections.defaultdict(int)
for file in dir_list:
    dict_color = collections.defaultdict(int)
    if file[-5]=="t":
        img = cv2.imread("data/"+file)
        for i in range(img.shape[0]):
             for j in range(img.shape[1]):
                 dict_color[tuple(img[i, j])] += 1
        class_num = []
        key_num = 0
        for keys,values in dict_color.items():
            class_num.append(values)
            key_num+=1
        dict_class[key_num] += 1
