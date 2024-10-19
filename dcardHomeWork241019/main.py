import os
import sys

from datetime import datetime


def main():

    # 初始字母清單
    names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    # 取得 names 的長度
    n = len(names)

    # 輸入數字
    # input_numbers = input("請輸入四個正整數，並用逗號分隔：")

    # 獲取正確的輸入
    while True:
        input_numbers = input("請輸入四個正整數，並用逗號分隔：")
        if validate_input(input_numbers, n):
            break

    # 轉換為整數列表
    input_numbers = list(map(int, input_numbers.split(',')))

    # 取得劃分位置
    split1 = input_numbers[0] - 1  # 第一個劃分點（索引需要減 1）
    split2 = input_numbers[1]      # 第二個劃分點（結束點）
    repeat_group1 = input_numbers[2]  # 第一個子清單的重複次數
    repeat_group3 = input_numbers[3]  # 第三個子清單的重複次數

    # 將 names 劃分成三個子清單
    group1 = names[:split1]  # 第一個子清單
    group2 = names[split1:split2]  # 第二個子清單
    group3 = names[split2:]  # 第三個子清單

    # 依據重複次數重複子清單中的元素
    group1_repeated = group1 * repeat_group1
    group3_repeated = group3 * repeat_group3

    # 組合新的字母清單
    new_list = group1_repeated + group2 + group3_repeated

    # 輸出結果
    print(new_list)


# 驗證輸入方法
def validate_input(user_input, n):
    try:
        # 檢查輸入格式是否符合"正整數,正整數,正整數,正整數"
        input_numbers = list(map(int, user_input.split(',')))
        # 檢查是否有四個數字
        if len(input_numbers) != 4:
            print("format invalid, correct format :: Integer,Integer,Integer,Integer")
            return False

        # 檢查每個數字是否都是正整數（大於零）
        for num in input_numbers:
            if num <= 0:
                print(
                    "format invalid, correct format :: Integer,Integer,Integer,Integer")
                return False

        # 檢查前兩個數字是否落在1到n之間
        if not (1 <= input_numbers[0] <= n) or not (1 <= input_numbers[1] <= n):
            print(f"前兩個數字必須落於 1 到 {n} 之間")
            return False

        # 檢查第2個數字是否不小於第1個數字
        if input_numbers[1] < input_numbers[0]:
            print("第二個數字不可以小於第一個數字")
            return False

        # 輸入正確
        return True
    except ValueError:
        print("format invalid, correct format :: Integer,Integer,Integer,Integer")
        return False


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
