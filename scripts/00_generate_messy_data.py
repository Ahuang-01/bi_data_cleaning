import pandas as pd
import numpy as np
import os

# 1. 确定存放路径 (兼容 Windows/Mac)
# __file__ 是当前脚本文件的路径，.parent.parent 回到项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'raw_sales_2024.xlsx')

def create_messy_excel():
    print("正在制造脏数据...")
    
    # 模拟 20 条数据
    data = {
        'order_id': [
            'ORD-001', 'ORD-002', 'ORD-003', np.nan, 'ORD-005', 
            'ORD-001', 'ORD-007', 'ORD-008', 'ORD-009', 'ORD-010',
            'ORD-011', 'ORD-012', 'ORD-013', 'ORD-014', 'ORD-015',
            'ORD-016', 'ORD-017', 'ORD-018', 'ORD-019', 'ORD-020'
        ],
        # 脏点1: 日期格式混乱，有斜杠、横杠、甚至中文
        'order_date': [
            '2024-01-01', '2024/01/02', '2024.01.03', '2024-01-04', '20240105',
            '2024-01-01', 'Jan 07, 2024', '2024-01-08', '2024/01/09', '2024-01-10',
            '2024-01-11', '2024/12/12', 'invalid_date', '2024-01-14', '2024-01-15',
            '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19', '2024-01-20'
        ],
        # 脏点2: 客户名大小写不一致，有空格
        'customer_name': [
            'Alice ', 'bob', 'Charlie', 'David', 'Eva',
            'Alice ', 'Frank', 'Grace', 'Heidi', 'Ivan',
            'Judy', 'Kevin', 'Lily', 'Mike', 'Nancy',
            'Oscar', 'Paul', 'Quinn', 'Rose', 'Steve'
        ],
        # 脏点3: 金额包含货币符号，且是字符串类型，还有缺失值
        'sales_amount': [
            '$100.50', '200', '$300', '400.0', '$500', 
            '$100.50', '700', None, '$900', '1000',
            '1100', '$1200', '1300', '$1400', '0',
            '-100', '1700', '$1800', '1900', '2000'
        ],
        # 脏点4: 地区写法不统一 (这是 BI 中最头疼的维度问题)
        'region': [
            'North', 'north', 'South', 'East', 'West',
            'North', 'South', 'East', 'West', 'North',
            'S.', 'East', 'West', 'North', 'South',
            'East', 'West', 'North', 'South', 'East'
        ]
    }
    
    df = pd.DataFrame(data)

    # 制造重复数据 (模拟 ORD-001 重复录入)
    # 这一步已经在 data 字典里手动加了重复的 Alice/ORD-001

    # 确保目录存在
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    
    # 保存为 Excel
    df.to_excel(RAW_DATA_PATH, index=False)
    print(f"✅ 脏数据生成完毕: {RAW_DATA_PATH}")

if __name__ == "__main__":
    create_messy_excel()