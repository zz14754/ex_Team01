# codes/raw_data_get.py
"""
原始数据抓取模块
一站式数据获取脚本（精简优化版）
输出文件：
  - data_raw/city_income.xlsx
  - data_raw/city_expenditure.xlsx
  - data_raw/individual_deposit.xlsx
  - data_raw/gdp.xlsx
  - data_raw/merged_raw.csv (填充后的经济数据)
  - data_raw/real_estate_raw.csv (房地产长格式数据)
"""
import requests
import json
import time
import pandas as pd
import urllib3
import os
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings()

def get_project_root_path():
    """返回项目根目录（当前文件所在目录的上一级）"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def fetch_stat_data(indicator_code, indicator_name, period="LAST20"):
    """从国家统计局API获取主要城市年度数据，返回长格式DataFrame"""
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
    print(f"正在抓取 {indicator_name} ({indicator_code})...", end=" ")
    try:
        response = requests.get(url, params=params, verify=False, timeout=15)
        data = response.json()
    except Exception as e:
        print(f"失败: {e}")
        return None
    if data.get("returncode") != 200:
        print(f"失败: {data.get('returnmsg', '未知错误')}")
        return None

    nodes = data["returndata"]["datanodes"]
    wdnodes = data["returndata"]["wdnodes"]

    # 解析地区代码和名称
    city_dict = {}
    for wdnode in wdnodes:
        if wdnode["wdcode"] == "reg":
            for node in wdnode["nodes"]:
                city_dict[node["code"]] = node["cname"]
    rows = []
    for node in nodes:
        wds = {w["wdcode"]: w["valuecode"] for w in node["wds"]}
        city_code = wds.get("reg", "")
        year_code = wds.get("sj", "")
        value = node["data"]["data"] if node["data"]["hasdata"] else None
        if value is not None:
            rows.append({
                "city": city_dict.get(city_code, city_code),
                "year": year_code,
                "value": value
            })
    df = pd.DataFrame(rows)
    print(f"成功，共 {df.shape[0]} 条记录。")
    return df


def save_as_pivot_excel(df, file_path, index_name):
    """将长表转换为以城市为行、年份为列的宽表，并保存为Excel"""
    if df is None or df.empty:
        return None
    pivot = df.pivot(index='city', columns='year', values='value')
    pivot.index.name = index_name
    pivot.to_excel(file_path)
    return pivot

def scrape_missing_city_data():
    """爬取缺失的城市统计数据（从统计公报网站），返回补全字典"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    missing_data = {}

    def fetch_page_content(url):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            for encoding in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
                try:
                    resp.encoding = encoding
                    text = resp.text
                    if '统计' in text or '公报' in text or '经济' in text:
                        return text
                except:
                    pass
            resp.encoding = resp.apparent_encoding
            return resp.text
        except Exception:
            return None

    def extract_plain_text(html):
        if not html:
            return ""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()

    def extract_number(text, keyword, unit='亿元'):
        if not text:
            return None
        pattern = rf'{keyword}[^。]*?([\d,]+\.?\d*)\s*{unit}'
        matches = re.findall(pattern, text)
        if matches:
            return float(matches[0].replace(',', ''))
        return None

    # --- 1. 哈尔滨 2022年 ---
    print("\n哈尔滨 2022")
    urls_harbin = [
        "http://www.tjcn.org/tjgb/07hlj/40339.html",
        "http://www.tjcn.org/tjgb/07hlj/40339_2.html",
    ]
    full_text = ""
    for url in urls_harbin:
        html = fetch_page_content(url)
        full_text += extract_plain_text(html)
    if full_text:
        income = extract_number(full_text, '一般公共预算收入')
        expend = extract_number(full_text, '一般公共预算支出')
    else:
        income = expend = None
    missing_data['哈尔滨_2022'] = {
        'income': income if income else 262.2,
        'expend': expend if expend else 1065.5,
    }

    # --- 2. 昆明 2009年 ---
    print("昆明 2009")
    url_km = "http://www.tjcn.org/tjgb/25yn/11727.html"
    html = fetch_page_content(url_km)
    km_text = extract_plain_text(html)
    income = extract_number(km_text, '一般预算收入')
    expend = extract_number(km_text, '一般预算支出')
    deposit = extract_number(km_text, '储蓄存款余额')
    missing_data['昆明_2009'] = {
        'income': income if income else 201.6125,
        'expend': expend if expend else 270.4495,
        'deposit': deposit if deposit else 1922.92,
    }

    # --- 3. 拉萨 2006年 ---
    print("拉萨 2006")
    url_ls_2006 = "https://web.xiaze.org/tjgb/201009/30764.html"
    html = fetch_page_content(url_ls_2006)
    ls_text = extract_plain_text(html)
    gdp = extract_number(ls_text, '生产总值')
    if gdp is None:
        gdp = extract_number(ls_text, '生产总值.*?GDP.*?')
    deposit = extract_number(ls_text, '储蓄存款')
    missing_data['拉萨_2006'] = {
        'gdp': gdp if gdp else 102.39,
        'deposit': deposit if deposit else 78.99,
    }

    # --- 4. 拉萨 2010年 ---
    print("拉萨 2010")
    url_ls_2010 = "http://www.tjcn.org/tjgb/26xz/20306.html"
    html = fetch_page_content(url_ls_2010)
    ls_text = extract_plain_text(html)
    gdp = extract_number(ls_text, '生产总值')
    deposit = extract_number(ls_text, '储蓄存款余额')
    if deposit is None:
        deposit = extract_number(ls_text, '储蓄存款')
    missing_data['拉萨_2010'] = {
        'gdp': gdp if gdp else 178.91,
        'deposit': deposit if deposit else 151.03,
    }

    # --- 5. 拉萨 2012年 ---
    print("拉萨 2012 ")
    missing_data['拉萨_2012'] = {'deposit': 223.83}

    # --- 6. 拉萨 2013年 ---
    print("拉萨 2013 ")
    missing_data['拉萨_2013'] = {'deposit': 272.12}

    return missing_data

def fill_missing_values(df, missing_dict):
    """用缺失字典中的数据填充DataFrame"""
    for key, values in missing_dict.items():
        city, year_str = key.rsplit("_", 1)
        year = int(year_str)
        mask = (df['city'] == city) & (df['year'] == year)
        if mask.any():
            for col, val in values.items():
                df.loc[mask, col] = val
        else:
            print(f"  警告: 未找到 {city} {year} 的记录，跳过。")
    return df

def main():
    root = get_project_root_path()
    data_raw = os.path.join(root, "data_raw")
    os.makedirs(data_raw, exist_ok=True)

    # ========== 1. 抓取基础经济指标 ==========
    economic_indicators = [
        ("A0401", "地方一般公共预算收入(亿元)", "income", "city_income.xlsx"),
        ("A0402", "地方一般公共预算支出(亿元)", "expend", "city_expenditure.xlsx"),
        ("A0403", "住户存款余额(亿元)", "deposit", "individual_deposit.xlsx"),
        ("A0101", "地区生产总值（当年价格）(亿元)", "gdp", "gdp.xlsx"),
    ]
    long_dfs = []
    for code, name, col, filename in economic_indicators:
        df = fetch_stat_data(code, name)
        if df is not None:
            file_path = os.path.join(data_raw, filename)
            save_as_pivot_excel(df, file_path, name)
            long_df = df.rename(columns={"value": col})[["city", "year", col]]
            long_dfs.append(long_df)
        time.sleep(1)

    # ========== 2. 抓取房地产指标（仅用于合并，不保存单个宽表） ==========
    real_estate_indicators = {
        "A0302": "房地产开发投资额(亿元)",
        "A0309": "商品房销售面积(万平方米)",
        "A030B": "商品房平均销售价格(元/平方米)",
        "A030A": "住宅商品房销售面积(万平方米)",
        "A030C": "住宅商品房平均销售价格(元/平方米)",
    }
    re_dfs = []
    for code, name in real_estate_indicators.items():
        df = fetch_stat_data(code, name)
        if df is not None:
            long_df = df.rename(columns={"value": code})[["city", "year", code]]
            re_dfs.append(long_df)
        time.sleep(1)

    # ========== 3. 合并经济数据 ==========
    if long_dfs:
        merged = long_dfs[0]
        for df in long_dfs[1:]:
            merged = merged.merge(df, on=["city", "year"], how="outer")
        merged_path = os.path.join(data_raw, "merged_raw.csv")
        merged.to_csv(merged_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ 合并经济数据已保存: {merged.shape}")
    else:
        merged_path = None
        print("⚠️ 未抓取到任何经济数据。")

    # ========== 4. 合并房地产数据 ==========
    if re_dfs:
        re_merged = re_dfs[0]
        for df in re_dfs[1:]:
            re_merged = re_merged.merge(df, on=["city", "year"], how="outer")
        re_path = os.path.join(data_raw, "real_estate_raw.csv")
        re_merged.to_csv(re_path, index=False, encoding="utf-8-sig")
        print(f"✅ 房地产数据已保存: {re_merged.shape}")
    else:
        print("⚠️ 未抓取到任何房地产数据。")

    # ========== 5. 爬取缺失数据 ==========
    print("\n🔍 正在爬取缺失数据...")
    missing = scrape_missing_city_data()
    # 不保存JSON，直接用于填充

    # ========== 6. 填充缺失数据 ==========
    if merged_path and os.path.exists(merged_path):
        df_merged = pd.read_csv(merged_path)
        df_merged['year'] = df_merged['year'].astype(int)
        print("\n📊 填充前缺失值统计:")
        print(df_merged.isnull().sum())

        df_filled = fill_missing_values(df_merged, missing)

        print("\n📊 填充后缺失值统计:")
        print(df_filled.isnull().sum())

        df_filled.to_csv(merged_path, index=False, encoding="utf-8-sig")
        print(f"✅ 更新后的 merged_raw.csv 已保存。")
    else:
        print("⚠️ merged_raw.csv 不存在，跳过填充步骤。")

    print("\n🎉 全部完成！")

if __name__ == "__main__":
    main()