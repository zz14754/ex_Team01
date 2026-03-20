# -*- coding: utf-8 -*-
"""执行 01_data_clean.ipynb 中的数据清洗逻辑"""
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW = os.path.join(project_root, "data_raw")
DATA_CLEAN = os.path.join(project_root, "data_clean")

# 1.1 读取原始数据
df = pd.read_csv(os.path.join(DATA_RAW, "merged_raw.csv"))
print(f"数据维度: {df.shape}")
print(f"城市数量: {df['city'].nunique()}")
print(f"年份范围: {df['year'].min()} - {df['year'].max()}")
print(f"城市列表: {sorted(df['city'].unique())}")

# 缺失值
print(f"\n各列缺失值:\n{df.isnull().sum()}")

# 1.2 数据清洗
df['year'] = df['year'].astype(int)
df = df[df['year'] <= 2024].copy()

# 删除核心指标全为空的行
df = df.dropna(subset=['income', 'expend', 'gdp'], how='all').copy()

# 计算预算缺口
df['gap'] = df['expend'] - df['income']
df['gap_to_gdp'] = df['gap'] / df['gdp']

# 1.3 计算增长率
df = df.sort_values(['city', 'year']).reset_index(drop=True)
for col in ['income', 'expend']:
    df[f'{col}_growth'] = df.groupby('city')[col].pct_change() * 100

# 1.4 城市分组
tier1 = ['北京', '上海', '广州', '深圳']
pearl_river = ['广州', '深圳', '珠海', '佛山', '东莞', '中山', '惠州']
yangtze_river = ['上海', '南京', '杭州', '苏州', '无锡', '宁波', '合肥', '南通']
pearl_available = [c for c in pearl_river if c in df['city'].unique()]
yangtze_available = [c for c in yangtze_river if c in df['city'].unique()]
print(f"\n珠三角可用城市: {pearl_available}")
print(f"长三角可用城市: {yangtze_available}")

def assign_group(city):
    if city in pearl_available:
        return '珠三角'
    elif city in yangtze_available:
        return '长三角'
    else:
        return '其他'

df['region_group'] = df['city'].apply(assign_group)
df['is_tier1'] = df['city'].isin(tier1)

# 1.5 保存
df.to_csv(os.path.join(DATA_CLEAN, "city_budget_clean.csv"), index=False, encoding="utf-8-sig")
print(f"\n主数据已保存: {df.shape}")

# 房地产数据
df_re = pd.read_csv(os.path.join(DATA_RAW, "real_estate_raw.csv"))
df_re['year'] = df_re['year'].astype(int)
df_re = df_re[df_re['year'] <= 2024].copy()
df_re.columns = ['city', 'year', 're_invest', 'sale_area', 're_avg_price', 'res_sale_area', 'res_avg_price']
df_re.to_csv(os.path.join(DATA_CLEAN, "real_estate_clean.csv"), index=False, encoding="utf-8-sig")
print(f"房地产数据已保存: {df_re.shape}")

# 合并
df_all = df.merge(df_re, on=['city', 'year'], how='left')
df_all.to_csv(os.path.join(DATA_CLEAN, "city_all_clean.csv"), index=False, encoding="utf-8-sig")
print(f"合并数据已保存: {df_all.shape}")
print(f"列: {df_all.columns.tolist()}")
print(f"\n数据描述统计:")
print(df[['income', 'expend', 'gdp', 'gap', 'gap_to_gdp']].describe())
