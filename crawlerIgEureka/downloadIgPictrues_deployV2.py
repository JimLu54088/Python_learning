import instaloader
import os
import sys
import shutil
from datetime import datetime


def main():
    print("----------Process started ------------")

    is_typeProfileManually = True
    is_typeTargetFolderManually = True

    # 指定你要下載的Instagram帳號
    if is_typeProfileManually:
        PROFILE = input("Please input ig profile(Ex:satohtakeruid): ")

    else:
        PROFILE = "kejing1004"

    # 指定Picture folder
    if is_typeTargetFolderManually:
        Origin_tARGET_DIR = input(
            "Please input Folder you want to put pictures in: ")

        TARGET_DIR = Origin_tARGET_DIR.replace("\\", "\\\\")

    else:
        TARGET_DIR = "D:/MyPython/crawlerIgEureka/downloadJinRU240721-2"

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
            raise ValueError("Please enter Y or N.")

        # is_downloadBetweenDates = input(
        #     "Do you want to download between dates?(Y/N) ")

        print("Please enter start date and end date, if no input the start date and end date will be set the bound of the account. ")
        str_download_startDate = input(
            "Please input start date  (format: YYYY-MM-DD): ")
        str_download_endDate = input(
            "Please input end date (format: YYYY-MM-DD): ")

        if not str_download_startDate and not str_download_endDate:
            print("Download all posts. ")
        elif str_download_startDate and not str_download_endDate:
            print(f"Downalod from {str_download_startDate} to Now")
        elif not str_download_startDate and str_download_endDate:
            print(f"Downalod from before to {str_download_endDate}")
        else:
            print(f"Downalod from {str_download_startDate} to {
                  str_download_endDate}")

        # 創建一個Instaloader實例
        L = instaloader.Instaloader(
            download_videos=bl_is_downloadVideos,  # 下載視頻?
            download_video_thumbnails=False,       # 不下載視頻縮略圖
            post_metadata_txt_pattern='',          # 不保存文本元數據
            save_metadata=False                    # 不保存JSON元數據
        )
        L.dirname_pattern = TARGET_DIR

        createIfnotExistDirAndCleanTargetDir(TARGET_DIR)

        # 加载用户资料
        profile = instaloader.Profile.from_username(L.context, PROFILE)

        for post in profile.get_posts():
            if not str_download_startDate and not str_download_endDate:
                L.download_post(post, target=TARGET_DIR)
            elif str_download_startDate and not str_download_endDate:

                dt_download_startDate = datetime.strptime(
                    str_download_startDate, "%Y-%m-%d")

                if dt_download_startDate <= post.date:
                    L.download_post(post, target=TARGET_DIR)
            elif not str_download_startDate and str_download_endDate:
                dt_download_endDate = datetime.strptime(
                    str_download_endDate, "%Y-%m-%d")

                if post.date <= dt_download_endDate:
                    L.download_post(post, target=TARGET_DIR)
            else:
                dt_download_startDate = datetime.strptime(
                    str_download_startDate, "%Y-%m-%d")
                dt_download_endDate = datetime.strptime(
                    str_download_endDate, "%Y-%m-%d")

                if dt_download_startDate <= post.date <= dt_download_endDate:
                    L.download_post(post, target=TARGET_DIR)

    except Exception as exception2:
        print(f"An error occurred: {exception2}", file=sys.stderr)


def createIfnotExistDirAndCleanTargetDir(TARGET_DIR):
    # 如果目標資料夾不存在，創建它
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # 清空目標資料夾
    try:
        shutil.rmtree(TARGET_DIR)
        # 如果需要保留基礎資料夾
        os.makedirs(TARGET_DIR)
        print(f"Deleted folder and its contents: {TARGET_DIR}")
    except Exception as common_exception:
        print(f"Error deleting folder {TARGET_DIR}: {common_exception}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
