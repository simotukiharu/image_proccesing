# 画像サイズが大きすぎるとき用にリサイズ
import os #コンピューター関連のライブラリ
import sys
import cv2
from PIL import Image, ImageFile
import numpy as np
import pathlib
import shutil

Image.MAX_IMAGE_PIXELS = 1000000000
ImageFile.LOAD_TRUNCATED_IMAGES = True
file_path = sys.argv[1]
dir_name = file_path
new_dir_name = '0_trigger_face_new'

files = sorted(os.listdir(dir_name))
# dst_dir = pathlib.Path('dst_layers')
# if(not dst_dir.exists()): dst_dir.mkdir() #フォルダがない時に作る

ml = 2000

for i in range(len(files)):
    file = files[i]
    
    # img = cv2.imread(os.path.join(dir_name, file), cv2.IMREAD_COLOR) 
    img = Image.open(os.path.join(dir_name, file))
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    width = img.shape[1]
    height = img.shape[0]
    if width < ml and height < ml:
        shutil.copy(os.path.join(dir_name, file), os.path.join(new_dir_name, file))
        print(file, 'copy')
        continue
    if width <= height:
        dst_width = int(width * (ml / height))
        img = cv2.resize(img, (dst_width, ml), interpolation= cv2.INTER_AREA)
        print(file, width, height, 'p')
    else:
        dst_height = int(height * (ml / width))
        img = cv2.resize(img, (ml, dst_height), interpolation= cv2.INTER_AREA)
        print(file, width, height, 'L')

    cv2.imwrite(os.path.join(new_dir_name, file), img)
    