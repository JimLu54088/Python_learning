import pandas as pd


def find_duplicates_in_csv():
    # 請求用戶輸入CSV檔案路徑
    file_path = input("請輸入CSV檔案路徑: ")

    try:
        # 讀取CSV檔案
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("找不到指定的文件，請檢查路徑後重新執行程式。")
        return
    except Exception as e:
        print(f"讀取文件時出現錯誤: {e}")
        return

    # 請求用戶輸入要檢查的兩個欄位索引
    try:
        column_index_1 = int(input("請輸入第一個要檢查的欄位索引(從0開始): "))
        column_index_2 = int(input("請輸入第二個要檢查的欄位索引(從0開始): "))
    except ValueError:
        print("請輸入有效的數字索引。")
        return

    # 檢查索引是否在範圍內
    if column_index_1 < 0 or column_index_1 >= len(df.columns) or column_index_2 < 0 or column_index_2 >= len(df.columns):
        print("索引超出範圍，請檢查後重新執行程式。")
        return

    # 取得指定索引的欄位名
    column_name_1 = df.columns[column_index_1]
    column_name_2 = df.columns[column_index_2]

    # 創建一個新欄位，將兩個欄位的值組合成一個字符串
    combined_column = df[column_name_1].astype(
        str) + "_" + df[column_name_2].astype(str)

    # 查找重複值
    duplicates = combined_column.value_counts()
    duplicates = duplicates[duplicates > 1]

    if duplicates.empty:
        print(f"欄位 '{column_name_1}' 和 '{column_name_2}' 組合後沒有重複的值。")
    else:
        print(f"欄位 '{column_name_1}' 和 '{column_name_2}' 組合後的重複值及其出現次數如下:")
        for value, count in duplicates.items():
            print(f"值: {value}, 出現次數: {count}")


if __name__ == "__main__":
    find_duplicates_in_csv()
