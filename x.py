import os
import shutil

# root / item / xx / img

# shutil.copyfile(r"C:\Users\Ryan\Desktop\1\x.txt", r"C:\Users\Ryan\Desktop\2\x.txt") #oldfile和newfile都只能是文件

root = '/home/s8/Desktop'

items = ['~5k', '~2.4w']

target = "/home/s8/Desktop/29kimg"

if not os.path.exists(target):
    os.mkdir(target)

for item in items:
    
    xx_list = []
    root_item = os.path.join(root, item)
    
    for dir_ in os.listdir(root_item):
        if os.path.isdir(os.path.join(root_item, dir_)):
            xx_list.append(os.path.join(root_item, dir_))
    
    for img_dir in xx_list:
        for file_ in os.listdir(img_dir):
            if file_.endswith('.jpg'):
                shutil.copyfile(os.path.join(img_dir, file_),
                                os.path.join(target, file_))
        print(img_dir, "OK")