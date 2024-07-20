import instaloader
import os
import sys
import shutil


def main():
    print("----------Process started ------------")

    is_typeProfileManually = True
    is_typeTargetFolderManually = True

    # 指定你要下載的Instagram帳號
    if is_typeProfileManually:
        PROFILE = input("Please input ig profile(Ex:satohtakeruid): ")

    else:
        PROFILE = "eureka_planet"

    # 指定Picture folder
    if is_typeTargetFolderManually:
        Origin_tARGET_DIR = input(
            "Please input Folder you want to put pictures in: ")

        TARGET_DIR = Origin_tARGET_DIR.replace("\\", "\\\\")

    else:
        TARGET_DIR = "D:\\MyPython\\crawlerIgEureka\\DownloadWithVideo"

    downloadIGPictureProcess(PROFILE, TARGET_DIR)

    print("----------Process finished ------------")


def downloadIGPictureProcess(PROFILE, TARGET_DIR):
    try:
        print("PROFILE: " + PROFILE)
        print("TARGET_DIR: " + TARGET_DIR + " Please check more!!!!!!!!!!!!!!")

        is_downloadVideos = input("Do you want to download videos?(Y/N) ")

        if is_downloadVideos == "Y":
            bl_is_downloadVideos = True

        elif is_downloadVideos == "N":
            bl_is_downloadVideos = False

        else:
            raise ValueError("Please enter Y or N. ")

        # 創建一個Instaloader實例
        L = instaloader.Instaloader(
            download_videos=bl_is_downloadVideos,  # 下載視頻?
            download_video_thumbnails=False,  # 不下載視頻縮略圖
            post_metadata_txt_pattern='',  # 不保存文本元數據
            save_metadata=False           # 不保存JSON元數據
        )

        # 如果目標資料夾不存在，創建它
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)

        # Clean TARGET_DIR
        try:
            shutil.rmtree(TARGET_DIR)
            # If base dir is still needed.
            os.makedirs(TARGET_DIR)

            print(f"Deleted folder and its contents: {TARGET_DIR}")
        except Exception as e:
            print(f"Error deleting folder {TARGET_DIR}: {e}")

        # 設置Instaloader的下載目標資料夾
        L.dirname_pattern = TARGET_DIR

        # 使用Instaloader下載該帳號的所有圖片（不包括其他元數據）
        L.download_profile(PROFILE, profile_pic_only=False)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
