
import os
import cv2

# 專案根目錄
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 資料夾路徑
INPUT_DIR = os.path.join(BASE_DIR, "input")
PREVIEW_DIR = os.path.join(BASE_DIR, "preview")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# YuNet 模型路徑
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "face_detection_yunet_2023mar.onnx"
)

# 人臉偵測信心門檻
CONFIDENCE_THRESHOLD = 0.7

# 紅色方框（OpenCV 使用 BGR 順序）
BOX_COLOR = (0, 0, 255)
BOX_THICKNESS = 3


def main():
    # 確認資料夾和模型存在
    if not os.path.isdir(INPUT_DIR):
        print(f"錯誤：找不到 input 資料夾：{INPUT_DIR}")
        return

    if not os.path.isfile(MODEL_PATH):
        print(f"錯誤：找不到 YuNet 模型：{MODEL_PATH}")
        return

    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # 支援的圖片格式
    extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    files = [
        name for name in os.listdir(INPUT_DIR)
        if name.lower().endswith(extensions)
    ]

    if not files:
        print("input 資料夾裡沒有照片。")
        return

    print("正在載入 YuNet 人臉偵測模型...")

    # 建立偵測器
    detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (320, 320),
        CONFIDENCE_THRESHOLD,
        0.3,
        5000
    )

    print("YuNet 模型載入成功。")
    print()

    total_faces = 0
    processed_count = 0

    for filename in sorted(files):
        image_path = os.path.join(INPUT_DIR, filename)

        image = cv2.imread(image_path)

        if image is None:
            print(f"[讀取失敗] {filename}")
            continue

        height, width = image.shape[:2]

        # YuNet 需要設定實際圖片尺寸
        detector.setInputSize((width, height))

        # 偵測人臉
        _, faces = detector.detect(image)

        # 建立預覽副本，避免修改原圖
        preview_image = image.copy()

        face_count = 0

        if faces is not None:
            for face in faces:
                # YuNet 回傳人臉框：
                # x、y、寬度、高度
                x = int(face[0])
                y = int(face[1])
                w = int(face[2])
                h = int(face[3])

                # 限制方框在圖片範圍內
                x1 = max(0, min(x, width - 1))
                y1 = max(0, min(y, height - 1))
                x2 = max(0, min(x + w, width - 1))
                y2 = max(0, min(y + h, height - 1))

                if x2 <= x1 or y2 <= y1:
                    continue

                # YuNet 的信心分數位於第 15 個欄位
                confidence = float(face[14])

                cv2.rectangle(
                    preview_image,
                    (x1, y1),
                    (x2, y2),
                    BOX_COLOR,
                    BOX_THICKNESS
                )

                label = f"Face {confidence:.2f}"
                text_y = max(y1 - 10, 25)

                cv2.putText(
                    preview_image,
                    label,
                    (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    BOX_COLOR,
                    2,
                    cv2.LINE_AA
                )

                face_count += 1

        # 儲存預覽圖片，不覆寫 input 中的原圖
        preview_path = os.path.join(PREVIEW_DIR, filename)

        if not cv2.imwrite(preview_path, preview_image):
            print(f"[儲存失敗] {filename}")
            continue

        total_faces += face_count
        processed_count += 1

        print(
            f"[完成] {filename}："
            f"偵測到 {face_count} 張臉，"
            f"預覽已儲存"
        )

    print()
    print(f"照片總數：{len(files)}")
    print(f"成功處理：{processed_count} 張")
    print(f"偵測到的人臉總數：{total_faces}")
    print(f"預覽資料夾：{PREVIEW_DIR}")
    print()
    print("原始照片沒有被修改。")


if __name__ == "__main__":
    main()
