# -*- coding: utf-8 -*-
"""
数据获取脚本：从国家统计局获取主要城市年度数据
数据来源: https://data.stats.gov.cn/easyquery.htm?cn=E0105
"""
import requests
import json
import time
import pandas as pd
import urllib3
import os
urllib3.disable_warnings()

DATA_RAW = r"D:\Project\City_Budget_Analysis\data_raw"

def fetch_city_data(indicator_code, indicator_name, period="LAST20"):
    """从国家统计局API获取主要城市年度数据"""
    url = "https://data.stats.gov.cn/easyquery.htm"
    params = {
        "m": "QueryData",
        "dbcode": "csnd",
        "rowcode": "reg",
        "colcode": "sj",
        "wds": json.dumps([{"wdcode": "zb", "valuecode": indicator_code}]),
        "dfwds": json.dumps([{"wdcode": "sj", "valuecode": period}]),
        "k1": str(time.time_ns())[:13],
    }
    print(f"Fetching {indicator_name} ({indicator_code})...")
    r = requests.get(url, params=params, verify=False)
    data = r.json()
    
    if data.get("returncode") != 200:
        print(f"  Error: {data}")
        return None
    
    nodes = data["returndata"]["datanodes"]
    wdnodes = data["returndata"]["wdnodes"]
    
    # 解析地区和时间维度
    reg_dict = {}
    sj_dict = {}
    for wdnode in wdnodes:
        if wdnode["wdcode"] == "reg":
            for n in wdnode["nodes"]:
                reg_dict[n["code"]] = n["cname"]
        elif wdnode["wdcode"] == "sj":
            for n in wdnode["nodes"]:
                sj_dict[n["code"]] = n["cname"]
    
    rows = []
    for node in nodes:
        wds = {w["wdcode"]: w["valuecode"] for w in node["wds"]}
        reg_code = wds.get("reg", "")
        sj_code = wds.get("sj", "")
        value = node["data"]["data"] if node["data"]["hasdata"] else None
        rows.append({
            "city_code": reg_code,
            "city": reg_dict.get(reg_code, reg_code),
            "year": sj_code,
            "value": value,
        })
    
    df = pd.DataFrame(rows)
    print(f"  Got {len(df)} records, {df['city'].nunique()} cities, years: {sorted(df['year'].unique())}")
    return df

# ============================================================
# 1. 财政和金融
# ============================================================

# 地方一般公共预算收入
df_income = fetch_city_data("A0401", "地方一般公共预算收入(亿元)")
time.sleep(1)

# 地方一般公共预算支出
df_expend = fetch_city_data("A0402", "地方一般公共预算支出(亿元)")
time.sleep(1)

# 住户存款余额
df_deposit = fetch_city_data("A0403", "住户存款余额(亿元)")
time.sleep(1)

# ============================================================
# 2. 国民经济核算
# ============================================================

# 地区生产总值
df_gdp = fetch_city_data("A0101", "地区生产总值（当年价格）(亿元)")
time.sleep(1)

# ============================================================
# 3. 房地产数据
# ============================================================

re_indicators = {
    "A0302": "房地产开发投资额(亿元)",
    "A0309": "商品房销售面积(万平方米)",
    "A030B": "商品房平均销售价格(元/平方米)",
    "A030A": "住宅商品房销售面积(万平方米)",
    "A030C": "住宅商品房平均销售价格(元/平方米)",
}

re_dfs = {}
for code, name in re_indicators.items():
    re_dfs[code] = fetch_city_data(code, name)
    time.sleep(1)

# ============================================================
# 保存原始数据
# ============================================================

def save_raw(df, filename, indicator_name):
    if df is not None:
        # 转为宽表格式 (城市 x 年份)
        pivot = df.pivot(index='city', columns='year', values='value')
        pivot.index.name = indicator_name
        filepath = os.path.join(DATA_RAW, filename)
        pivot.to_excel(filepath)
        print(f"Saved: {filepath} ({pivot.shape})")
        return pivot
    return None

save_raw(df_income, "city_income.xlsx", "地方一般公共预算收入(亿元)")
save_raw(df_expend, "city_expenditure.xlsx", "地方一般公共预算支出(亿元)")
save_raw(df_deposit, "individual_deposit.xlsx", "住户存款余额(亿元)")
save_raw(df_gdp, "gdp.xlsx", "地区生产总值(亿元)")

for code, name in re_indicators.items():
    safe_name = name.replace("(", "_").replace(")", "").replace("/", "_")
    save_raw(re_dfs[code], f"re_{code}_{safe_name}.xlsx", name)

# 同时保存长格式数据用于后续分析
all_long = []
for df, col_name in [(df_income, "income"), (df_expend, "expend"), 
                      (df_gdp, "gdp"), (df_deposit, "deposit")]:
    if df is not None:
        temp = df[["city", "year", "value"]].copy()
        temp.columns = ["city", "year", col_name]
        all_long.append(temp)

# 合并
merged = all_long[0]
for df in all_long[1:]:
    merged = merged.merge(df, on=["city", "year"], how="outer")

merged.to_csv(os.path.join(DATA_RAW, "merged_raw.csv"), index=False, encoding="utf-8-sig")
print(f"\nMerged data saved: {merged.shape}")
print(merged.head(10))

# 保存房地产长格式
re_long = None
for code, name in re_indicators.items():
    if re_dfs[code] is not None:
        temp = re_dfs[code][["city", "year", "value"]].copy()
        temp.columns = ["city", "year", code]
        if re_long is None:
            re_long = temp
        else:
            re_long = re_long.merge(temp, on=["city", "year"], how="outer")

if re_long is not None:
    re_long.to_csv(os.path.join(DATA_RAW, "real_estate_raw.csv"), index=False, encoding="utf-8-sig")
    print(f"\nReal estate data saved: {re_long.shape}")

print("\n=== Data fetching complete! ===")
