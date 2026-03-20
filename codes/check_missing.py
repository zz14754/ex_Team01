# -*- coding: utf-8 -*-
"""检查所有城市所有年份的缺失值情况"""
import pandas as pd
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW = os.path.join(project_root, "data_raw")

df = pd.read_csv(f"{DATA_RAW}/merged_raw.csv")
df['year'] = df['year'].astype(int)

# 排除2025年
df = df[df['year'] <= 2024]

# 检查每个城市每个指标的缺失
cols = ['income', 'expend', 'gdp', 'deposit']
print("="*80)
print("缺失值详细报告")
print("="*80)

for col in cols:
    missing = df[df[col].isnull()][['city', 'year', col]]
    if len(missing) > 0:
        print(f"\n--- {col} 缺失 ({len(missing)}条) ---")
        for _, row in missing.iterrows():
            print(f"  {row['city']} {row['year']}年")

# 同时检查房地产数据
df_re = pd.read_csv(f"{DATA_RAW}/real_estate_raw.csv")
df_re['year'] = df_re['year'].astype(int)
df_re = df_re[df_re['year'] <= 2024]
df_re.columns = ['city', 'year', 're_invest', 'sale_area', 're_avg_price', 'res_sale_area', 'res_avg_price']

print("\n\n--- 房地产数据缺失 ---")
for col in ['re_invest', 'sale_area', 're_avg_price']:
    missing = df_re[df_re[col].isnull()][['city', 'year']]
    if len(missing) > 0:
        print(f"\n{col} 缺失 ({len(missing)}条):")
        for _, row in missing.iterrows():
            print(f"  {row['city']} {row['year']}年")
