import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_DIR = os.path.abspath(__file__)
BASE_DIR_DIR2 = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data' , 'raw' , 'raw_sales_2024.xlsx')


print("Base directory is:", BASE_DIR)
print("Raw data path is:", RAW_DATA_PATH)
print("Raw data directory is:", os.path.dirname(RAW_DATA_PATH))
os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)# 确保目录存在
