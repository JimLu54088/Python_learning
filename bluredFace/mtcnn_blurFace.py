import cv2
import tensorflow as tf
from mtcnn import MTCNN

# 讀取影像
img = cv2.imread('D:\\MyPython\\imgProcess\\input\\20231008_185211.jpg')

# 初始化 MTCNN 偵測器
detector = MTCNN()

# 檢測人臉，MTCNN 的偵測器會直接在 RGB 圖像上進行偵測，所以需要轉換色彩空間
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
faces = detector.detect_faces(rgb_img)

# 檢測到的人臉數量
print(f"Detected {len(faces)} faces")

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

# 顯示並保存處理後的影像
cv2.imwrite('D:\\MyPython\\imgProcess\\input\\20231008_185211_blurred.jpg', img)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存處理後的影像
# cv2.imwrite('D:\\MyPython\\imgProcess\\output\\face_blurred.jpg', img)
