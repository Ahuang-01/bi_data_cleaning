import pandas as pd
import os
import sys

# === 1. 路径配置 (跨平台兼容写法) ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, 'data', 'raw', 'raw_sales_2024.xlsx')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'processed', 'cleaned_sales_2024.csv')

def clean_process():
    # 检查文件是否存在
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 错误: 找不到输入文件 {INPUT_FILE}，请先运行生成脚本。")
        return

    print(f"🔄 开始读取数据: {INPUT_FILE}...")
    df = pd.read_excel(INPUT_FILE)
    
    # 打印原始数据形状
    print(f"📊 原始数据行数: {df.shape[0]}, 列数: {df.shape[1]}")

    # === 2. 数据清洗逻辑 ===

    # [步骤 A] 处理重复值
    # 业务逻辑：如果 Order ID 相同，通常是系统重复录入，保留第一条即可
    initial_rows = len(df)
    df.drop_duplicates(subset=['order_id'], keep='first', inplace=True)
    print(f"✂️  删除了 {initial_rows - len(df)} 行重复数据")

    # [步骤 B] 处理缺失关键键 (Primary Key)
    # 业务逻辑：没有订单号的记录无法追踪，必须删除
    df.dropna(subset=['order_id'], inplace=True)

    # [步骤 C] 清洗金额列 (String -> Float)
    # 1. 转为字符串 2. 去掉 '$' 3. 转为数字 4. 处理非法值(coerce)
    print("🧹 正在清洗销售金额...")
    df['sales_amount'] = (
        df['sales_amount']
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False) # 防止有千分位逗号
    )
    df['sales_amount'] = pd.to_numeric(df['sales_amount'], errors='coerce')
    
    # 业务逻辑：销量不能为负数，简单处理为取绝对值，或者标记为异常
    df['sales_amount'] = df['sales_amount'].abs()
    
    # 填充金额缺失值 (假设业务规则是用 0 填充)
    df['sales_amount'] = df['sales_amount'].fillna(0.0)

    # [步骤 D] 标准化日期 (Date Parsing)
    # 这是一个难点，因为可能有各种格式。errors='coerce' 会把无法解析的变成 NaT (Not a Time)
    print("📅 正在标准化日期...")
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    
    # 删除那些日期完全无法解析的“垃圾行”
    df.dropna(subset=['order_date'], inplace=True)
    
    # 格式化为标准的 YYYY-MM-DD 字符串 (方便 CSV 阅读和数据库导入)
    df['order_date_str'] = df['order_date'].dt.strftime('%Y-%m-%d')

    # [步骤 E] 维度标准化 (String Manipulation)
    # 1. 客户名：去除首尾空格，首字母大写
    df['customer_name'] = df['customer_name'].str.strip().str.title()
    
    # 2. 地区：统一名称 (Mapping)
    # 业务场景：经常遇到缩写不一致，需要建立映射字典
    region_map = {
        'north': 'North',
        'south': 'South', 
        's.': 'South',    # 修正缩写
        'east': 'East',
        'west': 'West'
    }
    # 先转小写再映射，容错率更高
    df['region'] = df['region'].str.lower().map(region_map).fillna('Unknown')

    # === 3. 结果保存 ===
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 导出 CSV
    # index=False: 不保存 Pandas 的索引列
    # encoding='utf-8-sig': ⭐️ 关键！保证 Excel 打开 CSV 不乱码 (特别是中文环境)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"✅ 清洗完成！")
    print(f"📂 输出文件: {OUTPUT_FILE}")
    print(f"📊 最终有效数据行数: {len(df)}")
    print("-" * 30)
    
    # 简单预览
    print(df[['order_id', 'order_date_str', 'sales_amount', 'region']].head())

if __name__ == "__main__":
    clean_process()