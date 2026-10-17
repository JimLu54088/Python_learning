
##如果出現python 3.9 dll錯誤 

在cmd裡面輸入

set "PATH=D:\python_installation;D:\python_installation\Scripts;%PATH%"

python --version

看版本是不是正確



Step 1：進入專案資料夾
cd /d D:\MyPython\BlurFace_project

Step 2：建立虛擬環境
python -m venv .venv

啟用虛擬環境：
.venv\Scripts\activate

成功後，命令列前面通常會出現 (.venv)。

Step 3：安裝 OpenCV

python -m pip install --upgrade pip
python -m pip install opencv-python==4.10.0.84

確認安裝結果：
python -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'FaceDetectorYN'))"

應該看到類似：

4.10.0
True

執行
cd /d D:\MyPython\BlurFace_project

.venv\Scripts\python.exe mosaic_faces.py >> mosaic.log 2>&1

