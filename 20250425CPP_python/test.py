import ctypes

# 加載 DLL
cpptest = ctypes.CDLL(
    'D:/test_files/20250425_Cpp_test/cpptest/bin/Debug/cpptest.dll')

# 定義函數的參數和返回類型
cpptest.toLowerCase.argtypes = [ctypes.c_char_p]
cpptest.toLowerCase.restype = None  # 函數無返回值

# 傳入字符串並將其轉換為小寫
input_str = "HELLO WORLD"
input_str_buffer = ctypes.create_string_buffer(input_str.encode('utf-8'))

# 調用 DLL 函數
cpptest.toLowerCase(input_str_buffer)

# 輸出修改後的結果
print("Result:", input_str_buffer.value.decode('utf-8'))  # 應該輸出 "hello world"
