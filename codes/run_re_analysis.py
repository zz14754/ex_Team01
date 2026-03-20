# -*- coding: utf-8 -*-
"""执行 03_real_estate_analysis 的分析和可视化"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import warnings
warnings.filterwarnings('ignore')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_CLEAN = os.path.join(project_root, "data_clean")
OUTPUT = os.path.join(project_root, "output")

df = pd.read_csv(f"{DATA_CLEAN}/city_all_clean.csv")
print(f"数据: {df.shape}")

# 计算衍生指标
df['re_invest_to_gdp'] = df['re_invest'] / df['gdp']
df['sale_amount'] = df['sale_area'] * df['re_avg_price'] / 10000
df['sale_to_gdp'] = df['sale_amount'] / df['gdp']

# ============================================================
# 3.1 房地产投资与预算缺口的关系
# ============================================================
print("\n3.1 房地产投资与预算缺口的关系")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
valid = df.dropna(subset=['re_invest_to_gdp', 'gap_to_gdp'])
scatter = ax.scatter(valid['re_invest_to_gdp'], valid['gap_to_gdp'], 
                     c=valid['year'], cmap='viridis', alpha=0.5, s=20)
ax.set_xlabel('房地产投资/GDP')
ax.set_ylabel('gap_to_gdp')
ax.set_title('房地产投资强度 vs 预算缺口')
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='年份')

ax = axes[0, 1]
valid2 = df.dropna(subset=['sale_to_gdp', 'gap_to_gdp'])
scatter2 = ax.scatter(valid2['sale_to_gdp'], valid2['gap_to_gdp'], 
                      c=valid2['year'], cmap='viridis', alpha=0.5, s=20)
ax.set_xlabel('商品房销售额/GDP')
ax.set_ylabel('gap_to_gdp')
ax.set_title('商品房销售强度 vs 预算缺口')
ax.grid(alpha=0.3)
plt.colorbar(scatter2, ax=ax, label='年份')

ax = axes[1, 0]
avg_re = df.groupby('year')[['re_invest_to_gdp', 'gap_to_gdp']].mean()
ax2 = ax.twinx()
l1, = ax.plot(avg_re.index, avg_re['re_invest_to_gdp'], 'o-', color='#e74c3c', markersize=4, label='房地产投资/GDP')
l2, = ax2.plot(avg_re.index, avg_re['gap_to_gdp'], 's-', color='#3498db', markersize=4, label='gap_to_gdp')
ax.set_xlabel('年份')
ax.set_ylabel('房地产投资/GDP', color='#e74c3c')
ax2.set_ylabel('gap_to_gdp', color='#3498db')
ax.set_title('房地产投资强度与预算缺口趋势')
ax.legend(handles=[l1, l2], loc='upper left')
ax.grid(alpha=0.3)

tier1 = ['北京', '上海', '广州', '深圳']
ax = axes[1, 1]
for city in tier1:
    city_data = df[df['city'] == city]
    ax.plot(city_data['year'], city_data['re_avg_price'], marker='o', markersize=3, label=city)
ax.set_title('北上广深商品房平均销售价格')
ax.set_xlabel('年份')
ax.set_ylabel('元/平方米')
ax.legend()
ax.grid(alpha=0.3)

plt.suptitle('房地产与预算缺口关系分析', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/real_estate_gap_analysis.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: real_estate_gap_analysis.png")

# ============================================================
# 3.2 珠三角 vs 长三角 房地产对比
# ============================================================
print("\n3.2 珠三角 vs 长三角 房地产对比")

pearl_available = ['广州', '深圳']
yangtze_available = ['上海', '南京', '杭州', '宁波', '合肥']

df_pearl = df[df['city'].isin(pearl_available)]
df_yangtze = df[df['city'].isin(yangtze_available)]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
pearl_avg = df_pearl.groupby('year')['re_invest_to_gdp'].mean()
yangtze_avg = df_yangtze.groupby('year')['re_invest_to_gdp'].mean()
ax.plot(pearl_avg.index, pearl_avg.values, 'o-', label='珠三角', color='#e74c3c', markersize=4)
ax.plot(yangtze_avg.index, yangtze_avg.values, 's-', label='长三角', color='#3498db', markersize=4)
ax.set_title('房地产投资/GDP')
ax.set_xlabel('年份')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[0, 1]
pearl_price = df_pearl.groupby('year')['re_avg_price'].mean()
yangtze_price = df_yangtze.groupby('year')['re_avg_price'].mean()
ax.plot(pearl_price.index, pearl_price.values, 'o-', label='珠三角', color='#e74c3c', markersize=4)
ax.plot(yangtze_price.index, yangtze_price.values, 's-', label='长三角', color='#3498db', markersize=4)
ax.set_title('商品房平均销售价格(元/平方米)')
ax.set_xlabel('年份')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1, 0]
pearl_area = df_pearl.groupby('year')['sale_area'].mean()
yangtze_area = df_yangtze.groupby('year')['sale_area'].mean()
ax.plot(pearl_area.index, pearl_area.values, 'o-', label='珠三角', color='#e74c3c', markersize=4)
ax.plot(yangtze_area.index, yangtze_area.values, 's-', label='长三角', color='#3498db', markersize=4)
ax.set_title('商品房销售面积(万平方米)')
ax.set_xlabel('年份')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1, 1]
ax.scatter(df_pearl['re_invest_to_gdp'], df_pearl['gap_to_gdp'], 
           alpha=0.5, s=20, label='珠三角', color='#e74c3c')
ax.scatter(df_yangtze['re_invest_to_gdp'], df_yangtze['gap_to_gdp'], 
           alpha=0.5, s=20, label='长三角', color='#3498db')
ax.set_xlabel('房地产投资/GDP')
ax.set_ylabel('gap_to_gdp')
ax.set_title('房地产投资强度 vs 预算缺口(分区域)')
ax.legend()
ax.grid(alpha=0.3)

plt.suptitle('珠三角 vs 长三角 房地产与财政对比', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/pearl_yangtze_real_estate.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: pearl_yangtze_real_estate.png")

# ============================================================
# 3.3 时序特征分析
# ============================================================
print("\n3.3 时序特征分析")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

years = sorted(df['year'].unique())
corr_invest = []
corr_price = []
corr_sale = []
for y in years:
    ydata = df[df['year'] == y].dropna(subset=['re_invest_to_gdp', 'gap_to_gdp', 're_avg_price'])
    if len(ydata) > 5:
        corr_invest.append(ydata['re_invest_to_gdp'].corr(ydata['gap_to_gdp']))
        corr_price.append(ydata['re_avg_price'].corr(ydata['gap_to_gdp']))
        corr_sale.append(ydata['sale_area'].corr(ydata['gap_to_gdp']))
    else:
        corr_invest.append(np.nan)
        corr_price.append(np.nan)
        corr_sale.append(np.nan)

ax = axes[0]
ax.plot(years, corr_invest, 'o-', label='房地产投资/GDP', markersize=4)
ax.plot(years, corr_price, 's-', label='商品房价格', markersize=4)
ax.plot(years, corr_sale, '^-', label='销售面积', markersize=4)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('房地产指标与gap_to_gdp的相关系数')
ax.set_xlabel('年份')
ax.set_ylabel('相关系数')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[1]
pivot_re = df.pivot_table(index='city', columns='year', values='re_invest_to_gdp')
selected = ['北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉', '重庆', '天津']
selected = [c for c in selected if c in pivot_re.index]
pivot_sel = pivot_re.loc[selected]
im = ax.imshow(pivot_sel.values, aspect='auto', cmap='YlOrRd')
ax.set_yticks(range(len(selected)))
ax.set_yticklabels(selected, fontsize=8)
years_labels = [str(y) for y in pivot_sel.columns]
ax.set_xticks(range(0, len(years_labels), 2))
ax.set_xticklabels([years_labels[i] for i in range(0, len(years_labels), 2)], fontsize=7, rotation=45)
ax.set_title('房地产投资/GDP热力图')
plt.colorbar(im, ax=ax)

ax = axes[2]
df_sorted = df.sort_values(['city', 'year'])
df_sorted['re_invest_growth'] = df_sorted.groupby('city')['re_invest'].pct_change() * 100
df_sorted['gap_growth'] = df_sorted.groupby('city')['gap'].pct_change() * 100
avg_growth = df_sorted.groupby('year')[['re_invest_growth', 'gap_growth']].mean()
ax.plot(avg_growth.index, avg_growth['re_invest_growth'], 'o-', label='房地产投资增速', 
        color='#e74c3c', markersize=4)
ax.plot(avg_growth.index, avg_growth['gap_growth'], 's-', label='预算缺口增速', 
        color='#3498db', markersize=4)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('房地产投资增速 vs 预算缺口增速(%)')
ax.set_xlabel('年份')
ax.set_ylabel('增速(%)')
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT}/real_estate_time_series.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: real_estate_time_series.png")

# ============================================================
# 3.4 综合统计
# ============================================================
print("\n" + "="*60)
print("综合分析总结")
print("="*60)

df_2022 = df[df['year'] == 2022].dropna(subset=['gap_to_gdp'])
print(f"\n1. 2022年数据概览 ({len(df_2022)} 个城市)")
print(f"   gap_to_gdp 均值: {df_2022['gap_to_gdp'].mean():.4f}")
print(f"   gap_to_gdp 中位数: {df_2022['gap_to_gdp'].median():.4f}")
print(f"   gap_to_gdp 最大: {df_2022.loc[df_2022['gap_to_gdp'].idxmax(), 'city']} ({df_2022['gap_to_gdp'].max():.4f})")
print(f"   gap_to_gdp 最小: {df_2022.loc[df_2022['gap_to_gdp'].idxmin(), 'city']} ({df_2022['gap_to_gdp'].min():.4f})")

print(f"\n2. 2022年北上广深 gap_to_gdp:")
for city in tier1:
    val = df_2022[df_2022['city'] == city]['gap_to_gdp'].values
    if len(val) > 0:
        print(f"   {city}: {val[0]:.4f}")

print(f"\n3. 2022年区域对比:")
pearl_2022 = df_2022[df_2022['city'].isin(pearl_available)]['gap_to_gdp'].mean()
yangtze_2022 = df_2022[df_2022['city'].isin(yangtze_available)]['gap_to_gdp'].mean()
print(f"   珠三角平均 gap_to_gdp: {pearl_2022:.4f}")
print(f"   长三角平均 gap_to_gdp: {yangtze_2022:.4f}")

print(f"\n4. 2022年房地产相关:")
print(f"   房地产投资/GDP 均值: {df_2022['re_invest_to_gdp'].mean():.4f}")
corr = df_2022[['gap_to_gdp', 're_invest_to_gdp']].dropna().corr().iloc[0, 1]
print(f"   房地产投资/GDP 与 gap_to_gdp 相关系数: {corr:.4f}")

print("\n=== Real Estate Analysis Complete ===")
