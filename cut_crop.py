# 絵コンテを一カットずつに切り取る
import sys
sys.dont_write_bytecode = True
import pathlib
import cv2

# パスをコマンドライン引数で受け取る
targetDirPath = pathlib.Path(sys.argv[1]).resolve()
if not targetDirPath.is_dir(): exit() # ディレクトリのみ処理する

output_dir = pathlib.Path(sys.argv[2]) # 出力先のディレクトリ

# 指定されたディレクトリの"画像ファイル"一覧を取得
fileList = list(pathlib.Path(targetDirPath).iterdir())
fileList.sort()

# 間隔
# step_y = 100


# ターゲットのディレクトリ内を順にチェックしていく
exts = [".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG"]
for fn in fileList:
    if fn.is_file() and (fn.suffix in exts): # ファイルのみ処理する
        # print(fn)
        img = cv2.imread(str(fn)) # 画像ファイルの読み込み
        h = img.shape[0] 
        w = img.shape[1] 

                # 範囲内を細かく刻んで繰り返し処理してクロッピングを行う
        # 絵コンテの切り取る座標
        x0, y0 = 0, 0
        x1 = 563
        for i in range(5):
            y1 = int((i + 1) * h / 6)

            dst_img = img[y0 : y1, x0 : x1]
            print(fn.name, i, dst_img.mean())
            if 250 > dst_img.mean(): #平均濃度値が230より大きいものを保存しない
                outputfilename = output_dir / f"{fn.stem}_{i}.png"
                cv2.imwrite(str(outputfilename), dst_img)
            y0 = y1