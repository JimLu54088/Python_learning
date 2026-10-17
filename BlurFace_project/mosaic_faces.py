
import os
import cv2

# 專案根目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 資料夾路徑
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# YuNet 模型
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "face_detection_yunet_2023mar.onnx"
)

# 人臉信心門檻
#Normally use 0.7, together picture use 0.9
#CONFIDENCE_THRESHOLD = 0.9
CONFIDENCE_THRESHOLD = 0.7

# 馬賽克強度：數值越小，像素方塊越大
# 例如 12 代表把人臉縮小到約 12x12 像素再放大
MOSAIC_SIZE = 30

# 支援的圖片格式
EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def apply_mosaic(image, x1, y1, x2, y2):
    """將指定的人臉區域轉成像素化馬賽克。"""

    face = image[y1:y2, x1:x2]

    if face.size == 0:
        return

    face_height, face_width = face.shape[:2]

    # 縮小後的尺寸至少為 1x1
    small_width = max(1, face_width // MOSAIC_SIZE)
    small_height = max(1, face_height // MOSAIC_SIZE)

    # 使用最近鄰插值放大，保留方塊感
    small = cv2.resize(
        face,
        (small_width, small_height),
        interpolation=cv2.INTER_LINEAR
    )

    mosaic = cv2.resize(
        small,
        (face_width, face_height),
        interpolation=cv2.INTER_NEAREST
    )

    image[y1:y2, x1:x2] = mosaic


def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"錯誤：找不到 input 資料夾：{INPUT_DIR}")
        return

    if not os.path.isfile(MODEL_PATH):
        print(f"錯誤：找不到 YuNet 模型：{MODEL_PATH}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [
        name for name in os.listdir(INPUT_DIR)
        if name.lower().endswith(EXTENSIONS)
    ]

    if not files:
        print("input 資料夾裡沒有照片。")
        return

    print("正在載入 YuNet 模型...")

    detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (320, 320),
        CONFIDENCE_THRESHOLD,
        0.3,
        5000
    )

    print("模型載入成功。")
    print()

    total_faces = 0
    processed_count = 0

    for filename in sorted(files):
        input_path = os.path.join(INPUT_DIR, filename)

        # 讀取原始照片
        image = cv2.imread(input_path)

        if image is None:
            print(f"[讀取失敗] {filename}")
            continue

        height, width = image.shape[:2]
        detector.setInputSize((width, height))

        # 偵測人臉
        _, faces = detector.detect(image)

        face_count = 0

        if faces is not None:
            for face in faces:
                confidence = float(face[14])

                # 再次確認信心門檻
                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                x = int(face[0])
                y = int(face[1])
                w = int(face[2])
                h = int(face[3])

                # 限制範圍在照片內
                x1 = max(0, min(x, width - 1))
                y1 = max(0, min(y, height - 1))
                x2 = max(0, min(x + w, width))
                y2 = max(0, min(y + h, height))

                if x2 <= x1 or y2 <= y1:
                    continue

                # 僅對人臉區域套用馬賽克
                apply_mosaic(image, x1, y1, x2, y2)

                face_count += 1

        # 輸出使用原本檔名，原圖不會被覆寫
        output_path = os.path.join(OUTPUT_DIR, filename)

        success = cv2.imwrite(output_path, image)

        if not success:
            print(f"[儲存失敗] {filename}")
            continue

        total_faces += face_count
        processed_count += 1

        print(
            f"[完成] {filename}："
            f"處理 {face_count} 張臉"
        )

    print()
    print(f"照片總數：{len(files)}")
    print(f"成功輸出：{processed_count} 張")
    print(f"處理的人臉總數：{total_faces}")
    print(f"輸出資料夾：{OUTPUT_DIR}")
    print()
    print("原始照片未被修改。")


if __name__ == "__main__":
    main()
