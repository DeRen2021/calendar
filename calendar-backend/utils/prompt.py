import os
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file_as_string(file_path = os.path.join(BASE_DIR, "system_prompt.txt")):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        raise
    except IOError as e:
        print(f"读取文件 '{file_path}' 时出错: {str(e)}")
        raise