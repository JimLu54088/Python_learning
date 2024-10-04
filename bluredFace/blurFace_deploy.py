import cv2
import os
import sys
import tensorflow as tf
from mtcnn import MTCNN


def main():
    print("----------Process started ------------")

 # Type input folder

    intputFolder_origin = input("Please enter intputFolder Path : ")
    intpuFolderPath = intputFolder_origin.replace("\\", "\\\\")

    outputFolder_origin = input("Please enter outputFolder Path : ")
    outputFolderPath = outputFolder_origin.replace("\\", "\\\\")

    process_images_in_folder(intpuFolderPath, outputFolderPath)

    print("----------Process finished ------------")


# 主程式，處理資料夾中的所有圖片
def process_images_in_folder(input_folder, output_folder):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # # 讀取資料夾中的所有圖片文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # 可以根據需要增加其他圖片格式
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(
                output_folder, os.path.splitext(filename)[0] + '_blurred.jpg')

            # 調用函式來處理每張圖片
            blur_faces_in_image(image_path, output_path)


# 定義一個函式來模糊圖片中的人臉
def blur_faces_in_image(image_path, output_path):
    # 讀取影像
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Could not read image {image_path}")
        return

    # 初始化 MTCNN 偵測器
    detector = MTCNN()

    # 檢測人臉，MTCNN 的偵測器會直接在 RGB 圖像上進行偵測，所以需要轉換色彩空間
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb_img)

    # 檢測到的人臉數量
    print(f"Detected {len(faces)} faces in {image_path}")

    # 對每個檢測到的人臉進行處理
    for face in faces:
        # 提取人臉的邊界框
        x, y, w, h = face['box']

        # 確保邊界框的值不會超過影像範圍
        x, y = max(0, x), max(0, y)
        w, h = max(0, w), max(0, h)

        # 提取人臉區域
        face_region = img[y:y+h, x:x+w]

        # 對人臉區域進行模糊處理
        face_region_blurred = cv2.GaussianBlur(face_region, (151, 151), 75)

        # 將模糊後的人臉區域覆蓋回原影像
        img[y:y+h, x:x+w] = face_region_blurred

        # 保存模糊處理後的影像到指定文件
        cv2.imwrite(output_path, img)
        print(f"Saved blurred image to {output_path}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
