# -*- coding: utf-8 -*-
"""执行 02_EDA_analysis 和 03_real_estate_analysis 的分析和可视化"""
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import warnings
warnings.filterwarnings('ignore')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW = os.path.join(project_root, "data_raw")
DATA_CLEAN = os.path.join(project_root, "data_clean")
OUTPUT = os.path.join(project_root, "output")

df = pd.read_csv(f"{DATA_CLEAN}/city_budget_clean.csv")
print(f"数据: {df.shape}, 城市: {df['city'].nunique()}, 年份: {df['year'].min()}-{df['year'].max()}")

# ============================================================
# 2.1 特定年份 gap_to_gdp 最大和最小城市
# ============================================================
print("\n" + "="*60)
print("2.1 特定年份 gap_to_gdp 最大和最小城市")
print("="*60)

target_years = [2006, 2010, 2014, 2018, 2022]
results = []
for year in target_years:
    year_data = df[df['year'] == year].dropna(subset=['gap_to_gdp'])
    if len(year_data) == 0:
        continue
    max_row = year_data.loc[year_data['gap_to_gdp'].idxmax()]
    min_row = year_data.loc[year_data['gap_to_gdp'].idxmin()]
    results.append({
        '年份': year,
        'gap_to_gdp最大城市': max_row['city'],
        '最大值': round(max_row['gap_to_gdp'], 4),
        'gap_to_gdp最小城市': min_row['city'],
        '最小值': round(min_row['gap_to_gdp'], 4),
    })

result_df = pd.DataFrame(results)
print(result_df.to_string(index=False))
result_df.to_excel(f"{OUTPUT}/gap_to_gdp_extremes.xlsx", index=False)

# 可视化
fig, ax = plt.subplots(figsize=(12, 5))
x = range(len(target_years))
width = 0.35
bars1 = ax.bar([i - width/2 for i in x], result_df['最大值'], width, label='最大值', color='#e74c3c', alpha=0.8)
bars2 = ax.bar([i + width/2 for i in x], result_df['最小值'], width, label='最小值', color='#2ecc71', alpha=0.8)
for i, (bar, city) in enumerate(zip(bars1, result_df['gap_to_gdp最大城市'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, city, 
            ha='center', va='bottom', fontsize=9, rotation=30)
for i, (bar, city) in enumerate(zip(bars2, result_df['gap_to_gdp最小城市'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, city, 
            ha='center', va='bottom', fontsize=9, rotation=30)
ax.set_xticks(x)
ax.set_xticklabels(target_years)
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.set_title('各年度 gap_to_gdp 最大和最小城市')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/gap_to_gdp_extremes.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: gap_to_gdp_extremes.png")

# ============================================================
# 2.2 北上广深 gap_to_gdp 对比
# ============================================================
print("\n" + "="*60)
print("2.2 北上广深 gap_to_gdp 对比")
print("="*60)

tier1 = ['北京', '上海', '广州', '深圳']
df_tier1 = df[df['city'].isin(tier1)].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
for city in tier1:
    city_data = df_tier1[df_tier1['city'] == city]
    ax.plot(city_data['year'], city_data['gap_to_gdp'], marker='o', markersize=3, label=city)
ax.set_title('北上广深 gap_to_gdp 时序对比')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[0, 1]
for city in tier1:
    city_data = df_tier1[df_tier1['city'] == city]
    ax.plot(city_data['year'], city_data['gap'], marker='o', markersize=3, label=city)
ax.set_title('北上广深 预算缺口(gap) 时序对比')
ax.set_xlabel('年份')
ax.set_ylabel('预算缺口(亿元)')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1, 0]
for city in tier1:
    city_data = df_tier1[df_tier1['city'] == city]
    ax.plot(city_data['year'], city_data['income_growth'], marker='o', markersize=3, label=city)
ax.set_title('北上广深 财政收入增长率(%)')
ax.set_xlabel('年份')
ax.set_ylabel('增长率(%)')
ax.legend()
ax.grid(alpha=0.3)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)

ax = axes[1, 1]
for city in tier1:
    city_data = df_tier1[df_tier1['city'] == city]
    ax.plot(city_data['year'], city_data['expend_growth'], marker='o', markersize=3, label=city)
ax.set_title('北上广深 财政支出增长率(%)')
ax.set_xlabel('年份')
ax.set_ylabel('增长率(%)')
ax.legend()
ax.grid(alpha=0.3)
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)

plt.suptitle('北上广深财政数据对比分析', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/tier1_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: tier1_comparison.png")

# 打印北上广深关键数据
for city in tier1:
    cd = df_tier1[(df_tier1['city'] == city) & (df_tier1['year'] == 2022)]
    if len(cd) > 0:
        print(f"  {city} (2022): gap={cd['gap'].values[0]:.1f}亿, gap_to_gdp={cd['gap_to_gdp'].values[0]:.4f}")

# ============================================================
# 2.3 珠三角 vs 长三角
# ============================================================
print("\n" + "="*60)
print("2.3 珠三角 vs 长三角 gap_to_gdp 对比")
print("="*60)

pearl_available = ['广州', '深圳']
yangtze_available = ['上海', '南京', '杭州', '宁波', '合肥']
print(f"珠三角城市: {pearl_available}")
print(f"长三角城市: {yangtze_available}")

df_pearl = df[df['city'].isin(pearl_available)]
df_yangtze = df[df['city'].isin(yangtze_available)]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax = axes[0, 0]
for city in pearl_available:
    city_data = df_pearl[df_pearl['city'] == city]
    ax.plot(city_data['year'], city_data['gap_to_gdp'], marker='o', markersize=3, label=city)
ax.set_title('珠三角城市 gap_to_gdp')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[0, 1]
for city in yangtze_available:
    city_data = df_yangtze[df_yangtze['city'] == city]
    ax.plot(city_data['year'], city_data['gap_to_gdp'], marker='o', markersize=3, label=city)
ax.set_title('长三角城市 gap_to_gdp')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[1, 0]
pearl_avg = df_pearl.groupby('year')['gap_to_gdp'].mean()
yangtze_avg = df_yangtze.groupby('year')['gap_to_gdp'].mean()
ax.plot(pearl_avg.index, pearl_avg.values, marker='o', markersize=4, label='珠三角均值', color='#e74c3c', linewidth=2)
ax.plot(yangtze_avg.index, yangtze_avg.values, marker='s', markersize=4, label='长三角均值', color='#3498db', linewidth=2)
ax.set_title('珠三角 vs 长三角 平均 gap_to_gdp')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1, 1]
pearl_gap = df_pearl.groupby('year')['gap'].mean()
yangtze_gap = df_yangtze.groupby('year')['gap'].mean()
ax.plot(pearl_gap.index, pearl_gap.values, marker='o', markersize=4, label='珠三角均值', color='#e74c3c', linewidth=2)
ax.plot(yangtze_gap.index, yangtze_gap.values, marker='s', markersize=4, label='长三角均值', color='#3498db', linewidth=2)
ax.set_title('珠三角 vs 长三角 平均预算缺口(亿元)')
ax.set_xlabel('年份')
ax.set_ylabel('预算缺口(亿元)')
ax.legend()
ax.grid(alpha=0.3)

plt.suptitle('珠三角 vs 长三角 财政对比分析', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f"{OUTPUT}/pearl_vs_yangtze.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: pearl_vs_yangtze.png")

# ============================================================
# 2.4 全国城市 gap_to_gdp 分布与趋势
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
years_to_plot = [2006, 2010, 2014, 2018, 2022]
box_data = [df[df['year']==y]['gap_to_gdp'].dropna().values for y in years_to_plot]
bp = ax.boxplot(box_data, labels=years_to_plot, patch_artist=True)
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax.set_title('各年份 gap_to_gdp 分布(箱线图)')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
avg_gap = df.groupby('year')['gap_to_gdp'].agg(['mean', 'median', 'std'])
ax.plot(avg_gap.index, avg_gap['mean'], marker='o', markersize=4, label='均值', color='#e74c3c')
ax.plot(avg_gap.index, avg_gap['median'], marker='s', markersize=4, label='中位数', color='#3498db')
ax.fill_between(avg_gap.index, avg_gap['mean'] - avg_gap['std'], 
                avg_gap['mean'] + avg_gap['std'], alpha=0.2, color='#e74c3c')
ax.set_title('全国城市 gap_to_gdp 趋势')
ax.set_xlabel('年份')
ax.set_ylabel('gap_to_gdp')
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUTPUT}/gap_to_gdp_distribution.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: gap_to_gdp_distribution.png")

# ============================================================
# 2.5 收支增长率分析
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

avg_growth = df.groupby('year')[['income_growth', 'expend_growth']].mean()

ax = axes[0]
ax.plot(avg_growth.index, avg_growth['income_growth'], marker='o', markersize=4, 
        label='收入增长率', color='#2ecc71', linewidth=2)
ax.plot(avg_growth.index, avg_growth['expend_growth'], marker='s', markersize=4, 
        label='支出增长率', color='#e74c3c', linewidth=2)
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_title('全国城市平均财政收支增长率(%)')
ax.set_xlabel('年份')
ax.set_ylabel('增长率(%)')
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
valid = df.dropna(subset=['income_growth', 'expend_growth'])
scatter = ax.scatter(valid['income_growth'], valid['expend_growth'], 
                     c=valid['year'], cmap='viridis', alpha=0.4, s=15)
ax.plot([-50, 100], [-50, 100], 'r--', alpha=0.5, label='y=x')
ax.set_title('收入增长率 vs 支出增长率')
ax.set_xlabel('收入增长率(%)')
ax.set_ylabel('支出增长率(%)')
ax.legend()
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='年份')

plt.tight_layout()
plt.savefig(f"{OUTPUT}/growth_rate_analysis.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: growth_rate_analysis.png")

# ============================================================
# 2.6 2022年城市 gap_to_gdp 排名
# ============================================================
df_2022 = df[df['year'] == 2022].dropna(subset=['gap_to_gdp']).sort_values('gap_to_gdp', ascending=True)

fig, ax = plt.subplots(figsize=(10, 12))
colors = ['#e74c3c' if c in tier1 else 
          '#3498db' if c in pearl_available else 
          '#2ecc71' if c in yangtze_available else '#95a5a6' 
          for c in df_2022['city']]

ax.barh(range(len(df_2022)), df_2022['gap_to_gdp'], color=colors, alpha=0.8)
ax.set_yticks(range(len(df_2022)))
ax.set_yticklabels(df_2022['city'], fontsize=9)
ax.set_xlabel('gap_to_gdp')
ax.set_title('2022年各城市 gap_to_gdp 排名\n(红=一线 蓝=珠三角 绿=长三角 灰=其他)')
ax.grid(axis='x', alpha=0.3)
ax.axvline(x=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig(f"{OUTPUT}/gap_to_gdp_ranking_2022.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved: gap_to_gdp_ranking_2022.png")

print("\n=== EDA Analysis Complete ===")
