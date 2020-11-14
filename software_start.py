import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QButtonGroup,QApplication,QMainWindow,QDialog,QFileDialog,QProgressDialog,QMessageBox
from main import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from cut_pic import Cut_pic
from rename_filename import rename_filename
from google_translate import MyWindow
from mean_std_calc import Mean_Std
import pygame
import math
import cv2
class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self,text):
        self.textWritten.emit(str(text))

class MyMainWindow(QMainWindow,Ui_Form):
    def __init__(self):
        super(MyMainWindow,self).__init__()
        self.setupUi(self)

        self.num = 0
        # =============重定向输出框===============#
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)
        # ===========显示stackedWidget===========#
        self.cut_pic.clicked.connect(self.display_cut_pic)
        self.rename.clicked.connect(self.display_rename)
        self.conv_pool_calc.clicked.connect(self.display_conv_pool_calc)
        self.mean_std_calc.clicked.connect(self.display_mean_std)
        self.segmentation_label_operation.clicked.connect(self.display_segmentation_label)
        # ============切割图片模块============#
        self.Cut_choice.clicked.connect(self.openfile)
        self.Cut_work.clicked.connect(self.cut_work)
        # ============重命名模块===============#
        self.Rename_choice.clicked.connect(self.rename_openfile)
        self.Rename_start.clicked.connect(self.rename_start)
        self.replace_radioButton.toggled.connect(lambda:self.rename_radio(self.replace_radioButton))
        self.renew_radioButton.toggled.connect(lambda:self.rename_radio(self.renew_radioButton))
        # ============卷积池化计算器模块==========#
        self.conv_pool_calc_pushButton.clicked.connect(self.conv_pool_calc_start)
        self.conv_group_radio = QButtonGroup(self)
        self.conv_group_radio.addButton(self.conv_radioButton,1)
        self.conv_group_radio.addButton(self.pool_radioButton,2)
        self.conv_group_radio.buttonClicked.connect(self.conv_pool_calc_start)
        # ============谷歌翻译===================#
        self.google_transform.clicked.connect(self.display_google_transform)
        # ============数据集求均值和方差=========#

        self.mean_openfile_pushButton.clicked.connect(self.mean_std_openfile)
        self.mean_std_calc_pushButton.clicked.connect(self.mean_std_calc_start)

        # ============语义分割制作label=========#

        self.choose_RGB_label_pushButton.clicked.connect(self.choose_segmentation_label)
        self.cal_class_and_save_config.clicked.connect(self.generate_label_class)
        # ============数据集增强================#
        self.data_augmentation.clicked.connect(self.dispaly_data_augmentation)
        self.graphicsView_ori_image.setAcceptDrops(True)
        self.data_aug_openButton.clicked.connect(self.data_aug_openfile)
        self.data_aug_add_tran_Button.clicked.connect(self.data_aug_add_transpose)

        # =============开关背景音乐===============#
        self.Music_pushButton.clicked.connect(self.background_music)
        self.Music_flags = True
        pygame.init()
        track = pygame.mixer.music.load("./source/background.mp3")
        pygame.mixer.music.play()
    # ----------------背景音乐--------------------------------
    def background_music(self):
        self.Music_flags = bool(1-self.Music_flags)
        if (self.Music_flags == False):
            pygame.mixer.music.pause()
        if (self.Music_flags == True):
            pygame.mixer.music.unpause()

    def outputWritten(self, text):
        cursor = self.console_textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.console_textBrowser.setTextCursor(cursor)
        self.console_textBrowser.ensureCursorVisible()

    # -------------------切割图片--------------------
    def cut_work(self):
        global pic_path
        img_save_file = QFileDialog.getExistingDirectory(self, '保存文件', './')  # 存文件位置
        cut_w = int(self.Cut_w.text())
        cut_w_num = int(self.Cut_w_num.text())
        cut_h = int(self.Cut_h.text())
        cut_h_num = int(self.Cut_h_num.text())

        self.Cut_progressBar.setValue(0)
        self.Cut_progressBar.setMaximum(len(pic_path))
        self.Cut = Cut_pic(pic_path, cut_w,cut_w_num, cut_h, cut_h_num, img_save_file)
        self.Cut.update_data.connect(self.progress)
        self.Cut.start()

    def openfile(self):
        global pic_path
        fnames = QFileDialog.getOpenFileNames(self, '打开文件', './')
        if fnames[0]:
            for f in fnames[0]:
                self.Cut_textEdit.append(f)
        pic_path = fnames[0]

    def progress(self,msg):
        self.Cut_progressBar.setValue(msg)
        QApplication.processEvents()
        if msg==len(pic_path):
            QMessageBox.information(self,"提示","操作完毕！")

    # ------------------重命名------------------
    def rename_radio(self,btn):
        global img_save_file
        if btn.text()=="替换原有文件":
            if btn.isChecked()==True:
                img_save_file = rename_path
                print("新文件位置：{}".format(img_save_file))
            else:
                pass
        elif btn.text()=="保存到新的路径":
            if btn.isChecked()==True:
                img_save_file = QFileDialog.getExistingDirectory(self, '保存文件', './')
                print("新文件位置：{}".format(img_save_file))
            else:
                pass

    def rename_start(self):
        rename = self.Rename_lineEdit.text()
        tail_rename = self.Rename_lineEdit_2.text()
        print("您要的重命名{}_000001{}......已完毕".format(rename,tail_rename))
        global rename_path,img_save_file
        rename_filename(rename,rename_path,img_save_file,tail_rename)
        QMessageBox.information(self, "提示", "操作完毕！")

    def rename_openfile(self):
        global rename_path
        fname = QFileDialog.getExistingDirectory(self, '打开文件夹','./')
        rename_path = fname
        print("打开文件位置：{}".format(rename_path))

    # --------------------卷积池化计算器-------------------------------

    def conv_pool_calc_start(self):
        sender = self.sender()
        padding = int(self.padding_LineEdit.text())
        kernel_size = int(self.kernel_LineEdit.text())
        stride = int(self.stride_LineEdit.text())
        dialition = int(self.dialition_LineEdit.text())
        features = int(self.feature_size_LineEdit.text())
        result = math.floor((features-kernel_size+2*padding-(kernel_size-1)*(dialition-1))/stride)+1
        if sender==self.conv_group_radio:
            if self.conv_group_radio.checkedId()==1:
                str_head = "Conv"
                self.conv_show_plainTextEdit.setPlainText("{}:\nfeature:{}\nkernel_size:{}\nstride:{}\npadding:{}\ndialition:{}".format(str_head,features,kernel_size,stride,padding,dialition))
            else:
                str_head = "Pool"
                self.conv_show_plainTextEdit.setPlainText("{}:\nfeature:{}\nkernel_size:{}\nstride:{}\npadding:{}\ndialition:{}".format(str_head,features,kernel_size,stride,padding,dialition))
        elif sender==self.conv_pool_calc_pushButton:
            self.conv_show_plainTextEdit.appendPlainText("After Conv or Pool :{}".format(result))

# ----------------均值方差计算----------------------
    def mean_std_calc_start(self):
        global mean_std_path
        self.Mean_progressBar.setMaximum(len(mean_std_path))
        self.M_S = Mean_Std(mean_std_path)
        self.M_S.process_bar.connect(self.Mean_process)
        self.M_S.start()
        self.M_S.update_data.connect(self.Mean_callback)

    def Mean_process(self,msg):
        self.Mean_progressBar.setValue(msg)

    def Mean_callback(self,msg):
        self.Mean_R_lineEdit.setText(str(msg[0][0]))
        self.Mean_G_lineEdit.setText(str(msg[0][1]))
        self.Mean_B_lineEdit.setText(str(msg[0][2]))
        self.Std_R_lineEdit.setText(str(msg[1][0]))
        self.Std_G_lineEdit.setText(str(msg[1][1]))
        self.Std_B_lineEdit.setText(str(msg[1][2]))

    def mean_std_openfile(self):
        global mean_std_path
        fnames = QFileDialog.getOpenFileNames(self, '打开文件', './')
        if fnames[0]:
            for f in fnames[0]:
                self.mean_std_plainTextEdit.appendPlainText(f)
        mean_std_path = fnames[0]

# -------------------------语义分割制作label---------------------#

    def choose_segmentation_label(self):
        fnames = QFileDialog.getOpenFileNames(self, '打开label文件', './')
        if fnames[0]:
            for f in fnames[0]:
                self.RGB_label_path_textEdit.append(f)

    def generate_label_class(self):
        pass


# -------------------------图像增强---------------------#
    def data_aug_openfile(self):
        fnames  = QFileDialog.getOpenFileNames(self,'打开需要增强的图片','./')
        flag = True
        if fnames[0]:
            for j in fnames[0]:
                if flag==True:
                    img = cv2.imread(j)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    x = self.graphicsView_ori_image.width()
                    y = self.graphicsView_ori_image.height()
                    img = cv2.resize(img,(x,y))
                    frame = QImage(img,x,y,QImage.Format_RGB888)
                    pix = QPixmap.fromImage(frame)
                    item = QGraphicsPixmapItem(pix)
                    scene = QGraphicsScene()
                    scene.addItem(item)
                    self.graphicsView_ori_image.setScene(scene)
                    flag = False
                self.data_aug_showpath_plainTextEdit.appendPlainText(j)


    def data_aug_add_transpose(self):
        self.num+=1
        self.data_aug_transpose_listWidget.addItem("Item{}".format(self.num))
# --------------------- 显示模块-----------------------
    def display_cut_pic(self):
        '''
        :return:显示切割模块
        '''
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(1)
        print("您正在使用切割图片功能......")
    def display_rename(self):
        '''
        :return:重命名模块
        '''
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(0)
        print("您正在使用重命名功能......")
    def display_conv_pool_calc(self):
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(2)
        print("您正在使用卷积池化计算器功能......")

    def display_google_transform(self):
        self.console_textBrowser.clear()
        w = MyWindow()
        # 显示
        w.show()
        # 剪贴板对象
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(w.onClipboradChanged)
        print("您正在使用谷歌翻译功能......")

    def display_mean_std(self):
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(3)
        print("您正在使用计算数据集平均值和方差功能......")

    def display_segmentation_label(self):
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(4)
        print("您正在使用语义分割制作标签功能......")

    def dispaly_data_augmentation(self):
        self.console_textBrowser.clear()
        self.stackedWidget.setCurrentIndex(5)
        print("您正在使用数据集增强功能......")

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    my_software = MyMainWindow()
    my_software.show()

    sys.exit(app.exec_())