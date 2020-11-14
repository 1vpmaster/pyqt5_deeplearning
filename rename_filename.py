import os
import shutil
def rename_filename(rename,file_path,file_save_path,tail_rename):
    fileList = os.listdir(file_path)
    if file_save_path==file_path:
        for n,item in enumerate(fileList):
            oldname = file_path + os.sep +fileList[n]
            newname = file_path + os.sep +rename+"_"+str(n+1).zfill(6)+'.'+tail_rename
            os.rename(oldname,newname)
    else:
        for n,item in enumerate(fileList):
            oldname = file_path + os.sep + fileList[n]
            shutil.copy(oldname,file_save_path)
            newname = file_save_path + os.sep + rename + "_" + str(n + 1).zfill(6) + '.' + tail_rename
            os.rename(oldname, newname)



