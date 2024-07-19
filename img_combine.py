# 第3者への評価実験用に画像を並べる
import cv2
import sys
import pathlib
import numpy as np

def resize_caption(src, ml, cap_txt): #関数を定義
    height, width, _ = src.shape #縦横のシェイプを取得
    print(width, height)
    resize_width = int(width * (ml / height)) #横幅の長さをリサイズ
    resize_img = (resize_width, ml) #サイズ画像の横と縦を代入 ＃たては400に固定
    print(resize_img)

    dst = cv2.resize(src, (resize_width, ml)) #リサイズした画像をdstに代入
    caption = np.ones((30, resize_width, 3), np.uint8) * 255 #空の画像を作る
    cv2.putText(caption, cap_txt, (resize_width // 2, 25), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0))
    cv2.rectangle(dst, (0,0), (resize_width-1, ml-1), (0, 0, 0))
    dst_v = cv2.vconcat([dst, caption])
    return dst_v

exts = [".jpg", ".png", ".jpeg", ".bmp", ".webp", ".JPG", ".PNG", ".JPEG", ".BMP", ".WEBP", '.psd', '.PSD']
dir_path = pathlib.Path(sys.argv[1])
src_paths_1 = sorted([p for p in dir_path.iterdir() if p.suffix in exts])
dir_path = pathlib.Path(sys.argv[2])
src_paths_2 = sorted([p for p in dir_path.iterdir() if p.suffix in exts])
dst_folder = pathlib.Path(sys.argv[3])
if(not dst_folder.exists()): dst_folder.mkdir()

for i in range(len(src_paths_1)):
    img_1 = cv2.imread(str(src_paths_1[i]))
    img_2 = cv2.imread(str(src_paths_2[i]))
    
    ml = 400 #最大サイズ
    if i % 2 == 0:
        dst_1 = resize_caption(img_1,ml, 'A')
        dst_2 = resize_caption(img_2,ml, 'B')
    else:
        dst_1 = resize_caption(img_2,ml, 'A')
        dst_2 = resize_caption(img_1,ml, 'B') #画像を逆順に

    spacer = np.ones((ml + 30, 30,  3), np.uint8) * 255
    dst_h = cv2.hconcat([dst_1, spacer, dst_2])

    cv2.imwrite(f'{dst_folder}/{i:03}.png', dst_h)