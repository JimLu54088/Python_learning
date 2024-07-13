import os
import sys
import time

def delete_files_in_folder(folder_path):
    # 检查输入的路径是否是文件夹
    if not os.path.isdir(folder_path):
        print("Input path is not a directory. Exit.")
        sys.exit()

    # 初始化计数器
    deleted_file_count = 0

    # 遍历文件夹中的所有子文件夹和文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Delete file: {file_path}")
                deleted_file_count+=1
            except Exception as e:
                print(f"Failed to Delete file: {file_path}, ERROR: {e}")

    # 返回删除的文件数目
    return deleted_file_count

if __name__ == "__main__":
    folder_path = input("Please input a directory: ")
    deleted_count = delete_files_in_folder(folder_path)
    if deleted_count == 0:
       print("No file be deleted.")

    print("Wait for 3 seconds...")
    time.sleep(3)
