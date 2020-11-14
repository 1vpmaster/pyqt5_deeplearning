from main import *
from PIL import Image


class Cut_pic(QtCore.QThread):
    update_data = QtCore.pyqtSignal(int)
    def __init__(self,filename,pic_w, pic_w_num, pic_h, pic_h_num, img_save_file):
        super(Cut_pic,self).__init__()
        self.filename = filename
        self.pic_w = pic_w
        self.pic_w_num = pic_w_num
        self.pic_h = pic_h
        self.pic_h_num = pic_h_num
        self.img_save_file = img_save_file
    def run(self):
        i = 0
        for item in self.filename:
            img = Image.open(item)
            name = item.split("/")[-1][:-4]
            tail = item.split("/")[-1][-4:]
            self.cutpic(img, self.pic_w, self.pic_w_num, self.pic_h, self.pic_h_num, self.img_save_file,name,tail)
            i+=1
            self.update_data.emit(i)

    def cutpic(self,img, cut_x, cut_x_num, cut_y, cut_y_num, path, name,tail,t=0):  # 输入待切割的图片和需要切割的大小

        width = img.size[0]
        height = img.size[1]
        dx = cut_x - int((cut_x_num*cut_x - width)/(cut_x_num-1))
        dy = cut_y - int((cut_y_num * cut_y - height) / (cut_y_num - 1))

        x1 = 0
        y1 = 0
        x2 = cut_x
        y2 = cut_y
        num = 0 + t
        while x2 <= width:
            while y2 <= height:
                img2 = img.crop((x1, y1, x2, y2))
                num += 1
                path1 = path + "/" + name+"_"+str(num) + tail
                img2.save(path1)
                y1 += dy
                y2 = y1 + cut_y
            x1 = x1 + dx
            x2 = x1 + cut_x
            y1 = 0
            y2 = cut_y
        print("切割图片个数", num)
        return (height // dx) * (width // dy)
