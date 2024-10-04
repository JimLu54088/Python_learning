import cv2

img = cv2.imread('D:\\MyPython\\imgProcess\\input\\20231008_155901.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier('face_detect.xml')
# faceRect = faceCascade.detectMultiScale(gray, 1.1, 3)
faceRect = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,  # 調低 scaleFactor 可以檢測到更多人臉
    minNeighbors=1,   # 減少 minNeighbors
    # minSize=(30, 30)  # 設置最小人臉尺寸
)


print(len(faceRect))

# for (x, y, w, h) in faceRect:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
# 對每個檢測到的人臉進行處理
for (x, y, w, h) in faceRect:
    # 提取人臉區域
    face_region = img[y:y+h, x:x+w]

    # 對人臉區域進行模糊處理
    face_region_blurred = cv2.GaussianBlur(face_region, (51, 51), 30)

    # 將模糊後的人臉區域覆蓋回原影像
    img[y:y+h, x:x+w] = face_region_blurred

# # 保存模糊處理後的影像到文件
# # cv2.imwrite('C:\\Users\\Jim\\Desktop\\face_blurred.jpg', img)

cv2.imshow('img', img)
cv2.waitKey(0)

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
#         cv2.imshow('video', frame)
#     else:
#         break
#     if cv2.waitKey(1) == ord('q'):
#         break
# print(img.shape)

# while True:
#     ret, frame = cap.read()
#     if ret:
#         # 調整影像大小
#         frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)

#         # 將影像轉為灰階（Canny 邊緣檢測要求單通道灰階圖像）
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # 應用 Canny 邊緣檢測
#         edges = cv2.Canny(gray_frame, 100, 200)

#         # 顯示 Canny 邊緣檢測的結果
#         cv2.imshow('Canny Edge Detection', edges)
#     else:
#         break

#     # 按下 'q' 鍵退出
#     if cv2.waitKey(1) == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
