import random
import time


def roll_dice_simulation():
    # 使用者輸入執行次數
    try:
        num_rolls = int(input("請輸入擲骰子的次數："))
        if num_rolls <= 0:
            print("請輸入一個正整數！")
            return
    except ValueError:
        print("請輸入一個有效的正整數！")
        return

    # 建立一個字典來記錄點數出現次數
    dice_counts = {i: 0 for i in range(1, 7)}

    # 模擬擲骰子
    start_time = time.time()
    for _ in range(num_rolls):
        roll = random.randint(1, 6)
        dice_counts[roll] += 1
    end_time = time.time()
    execution_time = end_time - start_time

    # 輸出結果
    print("\n擲骰子結果：")
    for number, count in dice_counts.items():
        percentage = (count / num_rolls) * 100
        print(f"{number} 出現 {count} 次，比例：{percentage:.1f}%")
    print(f"執行時間：{execution_time:.4f} 秒")


if __name__ == "__main__":
    roll_dice_simulation()
