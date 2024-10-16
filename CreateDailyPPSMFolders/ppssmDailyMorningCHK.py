import sys
import argparse
import os
from property_loader import PropertyLoader
from datetime import datetime
from datetime import datetime, timedelta
import re
import shutil


def main():
    print("----------Process started ------------")

    parser = argparse.ArgumentParser(description='Process property file.')
    parser.add_argument('property_file', type=str,
                        help='Path to the property file')

    args = parser.parse_args()

    if not args.property_file:
        print("ERROR: Property File Name is not given. Please provide info -Dproperty.file=<Path of property file>", file=sys.stderr)
        sys.exit(-1)

    PropertyLoader.property_file_path = args.property_file
    PropertyLoader.load_properties()

    # 獲取絕對路徑
    absolute_property_file_path = os.path.abspath(args.property_file)
    print(f"Property file absolute path: {absolute_property_file_path}")

    createppsmDailyReportFolderAndDeleteOldFolders()

    createWebLogTodayDateFolder()

    cleanFolders()

    print("----------Process finished ------------")


def createppsmDailyReportFolderAndDeleteOldFolders():
    print("----------createppsmDailyReportFolderAndDeleteOldFolders Process started ------------")
    # Create PPSM daily report folder yyyyMMdd

    # get target folder path
    ppsmDailyReportGeneratedFolder = PropertyLoader.get_property(
        "ppsmDailyReportGeneratedFolder")

    # 取得今天的日期，格式為 YYYYMMDD
    today_date_formatter_yyyymmdd = datetime.now().strftime('%Y%m%d')

    # print(f"today date is: {today_date_formatter_yyyymmdd}")

    # Get new ppsmDailyReporPath
    ppsmDailyReporPath = os.path.join(ppsmDailyReportGeneratedFolder,
                                      today_date_formatter_yyyymmdd)

    # check if ppsmDailyReporPath already exist or not
    if not os.path.exists(ppsmDailyReporPath):
        os.makedirs(ppsmDailyReporPath)
        print(f"Directory {ppsmDailyReporPath} created.")
    else:
        print(f"Directory {ppsmDailyReporPath} already exists.")

    three_days_ago = datetime.now().date() - timedelta(days=3)

    # 列出目标目录下的所有文件夹
    foldersInppsmDailyReportGeneratedFolder = os.listdir(
        ppsmDailyReportGeneratedFolder)

    # 正则表达式匹配日期格式 YYYYMMDD
    date_pattern = re.compile(r'^\d{8}$')

    for folder_name in foldersInppsmDailyReportGeneratedFolder:
        if date_pattern.match(folder_name):
            folder_date = datetime.strptime(folder_name, '%Y%m%d').date()

            # 如果文件夹日期早于三天前的日期，则删除文件夹
            if folder_date <= three_days_ago:
                folder_path = os.path.join(
                    ppsmDailyReportGeneratedFolder, folder_name)
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old folder: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")
    print("----------createppsmDailyReportFolderAndDeleteOldFolders Process end ------------")


def createWebLogTodayDateFolder():
    print("----------createWebLogTodayDateFolder Process started ------------")

    # get target folder path
    WebJbossServerLogFolder = PropertyLoader.get_property(
        "WebJbossServerLogFolder")

    today_date_formatter_yymmdd = datetime.now().strftime('%y%m%d')  # YYMMDD
    # print(f"today's value : {today_date_formatter_yymmdd}")

    # Get new webLogpath
    webLogpath = os.path.join(WebJbossServerLogFolder,
                              today_date_formatter_yymmdd)

    # check if ppsmDailyReporPath already exist or not
    if not os.path.exists(webLogpath):
        os.makedirs(webLogpath)
        print(f"Directory {webLogpath} created.")
    else:
        print(f"Directory {webLogpath} already exists.")

    three_days_ago = datetime.now().date() - timedelta(days=int(PropertyLoader.get_property(
        "nDaysAgo")))

    print(f"Clear folder before Date:  {three_days_ago}")

    # 列出目标目录下的所有文件夹
    foldersInWebJbossServerLog = os.listdir(
        WebJbossServerLogFolder)

    # 正则表达式匹配日期格式 YYYYMMDD
    date_pattern = re.compile(r'^\d{6}$')

    for folder_name in foldersInWebJbossServerLog:
        if date_pattern.match(folder_name):
            folder_date = datetime.strptime(folder_name, '%y%m%d').date()

            # 如果文件夹日期早于三天前的日期，则删除文件夹
            if folder_date <= three_days_ago:
                folder_path = os.path.join(
                    WebJbossServerLogFolder, folder_name)
                try:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old folder: {folder_path}")
                except OSError as e:
                    print(f"Error deleting folder {folder_path}: {e}")
    print("----------createWebLogTodayDateFolder Process end ------------")


def cleanFolders():
    print("----------cleanFolders Process started ------------")
    foldersToBeClean = PropertyLoader.get_property(
        "folderToBeClean")
    # print(f"foldersToBeClean: {foldersToBeClean}")

    folder_paths = [folder.strip() for folder in foldersToBeClean.split(',')]

    for folder_path in folder_paths:
        try:
            shutil.rmtree(folder_path)
            # If base dir is still needed.
            os.makedirs(folder_path)

            print(f"Deleted folder and its contents: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder {folder_path}: {e}")

    print("----------cleanFolders Process end ------------")


# def cleanFoldersProcess(folder_paths):

#     for folder_path in folder_paths:
#         try:
#             # 清空文件夹内容
#             for root, dirs, files in os.walk(folder_path):
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     os.remove(file_path)
#                 for dir in dirs:
#                     dir_path = os.path.join(root, dir)
#                     os.rmdir(dir_path)
#             print(f"Cleared folder: {folder_path}")
#         except Exception as e:
#             print(f"Error clearing folder {folder_path}: {e}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
