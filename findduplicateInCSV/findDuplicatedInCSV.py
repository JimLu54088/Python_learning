import pandas as pd


def find_duplicates_in_csv():
    # 請求用戶輸入CSV檔案路徑
    file_path = input("Please input csv file path: ")

    try:
        # 讀取CSV檔案
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Cannot find the csv file, please check.")
        return
    except Exception as e:
        print(f"讀取文件時出現錯誤: {e}")
        return

    # 請求用戶輸入要檢查的欄位索引
    try:
        column_index = int(input("Please input the index(from 0): "))
    except ValueError:
        print("Please input valid integer. ")
        return

    # 檢查索引是否在範圍內
    if column_index < 0 or column_index >= len(df.columns):
        print("Index out of bound. Please re-enter. ")
        return

    # 取得指定索引的欄位名
    column_name = df.columns[column_index]

    # 查找重複值
    duplicates = df[column_name].value_counts()
    duplicates = duplicates[duplicates > 1]

    # if duplicates.empty:
    #     print(f"Column '{column_name}' No duplicated found. ")
    # else:
    #     print(f"Column '{column_name}' 中的重複值及其出現次數如下:")
    #     print(duplicates)

    if duplicates.empty:
        print(f"Column '{column_name}' No duplicated found.")
    else:
        print(f"Column '{column_name}' Found duplicated value in below\n")
        for value, count in duplicates.items():
            print(f"value: {value}, Duplicated Count: {count}")


if __name__ == "__main__":
    find_duplicates_in_csv()
    print("\n")
