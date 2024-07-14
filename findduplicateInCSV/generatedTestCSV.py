import pandas as pd
import random
import string
import time
import os


def generate_vin():
    prefix = random.choice(["SJK", "WDD"])
    suffix = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=14))
    return prefix + suffix


def generate_ecu_or_ecu_val():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_data(num_records):
    data = {
        "VIN": [generate_vin() for _ in range(num_records)],
        "ECU": [generate_ecu_or_ecu_val() for _ in range(num_records)],
        "ECU_VAL": [generate_ecu_or_ecu_val() for _ in range(num_records)]
    }
    return data


def main():
    # num_records = 10000000
    str_num_records = input(
        "Please enter how many rows do you want to generate for test.\n")
    csv_base_dir = input(
        "Please enter a directory that you want to put the csv in.\n")

    file_path = os.path.join(csv_base_dir, "Book22.csv")

    if os.path.exists(file_path):
        os.remove(file_path)

    num_records = int(str_num_records)

    # file_path = "D:/MyPython/findduplicateInCSV/Book2.csv"

    # 開始計時
    start_time = time.time()

    # 生成數據
    data = generate_data(num_records)

    # 創建 DataFrame
    df = pd.DataFrame(data)

    # 將 DataFrame 寫入 CSV 文件
    df.to_csv(file_path, index=False)
    print(f"已成功生成 {num_records} 筆資料並寫入 {file_path}")

    # 結束計時
    end_time = time.time()

    # 計算程式執行時間
    execution_time = end_time - start_time
    print(f"The time between enter the count of rows and generated csv: {
          execution_time:.4f} seconds")


if __name__ == "__main__":

    main()
