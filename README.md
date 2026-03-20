# 中国主要城市公共预算支出和收入数据分析

![](https://img.shields.io/badge/Language-Python-blue) ![](https://img.shields.io/badge/Status-Active-green) ![](https://img.shields.io/badge/License-Academic-orange)

**项目选题：** T2 - 中国主要城市公共预算支出和收入数据分析  
**班级：** 25MDE PC  
**组号：** G1  
**组员：** 钟梅（组长）、王海林、王晓航、吴惠彪、梁小婵、梁佩文、章翔宇、曾铮  
**最后更新：** 2026年3月20日

---

## 📋 目录

- [项目概述](#项目概述)
- [数据说明](#数据说明)
- [分析内容](#分析内容)
- [主要发现](#主要发现)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [更新日志](#更新日志)
- [许可证](#许可证)

中国城市财政预算收支失衡已成为常态。改革开放以来，中央财政转移支付制度与地方财政收支不平衡问题长期存在，尤其在经济下行期、金融危机与疫情冲击时期，**预算缺口（支出>收入）** 更为显著。理解这一现象的规律性、区域特征和时间动态，对制定科学的转移支付政策、财政补助标准和地方债券额度具有重要意义。
研究范围
- **城市覆盖**：中国36个主要城市（包括一线城市、区域中心、主要地级市）
- **区域分组**：珠三角地区、长三角地区、其他地区
- **时间跨度**：2006-2024年，共19年（包括2008金融危机、2015经济调整、2020疫情冲击、2021复苏阶段）
---

# 三、数据说明

## （一）数据来源

### 1. 主要数据源

国家统计局 - 主要城市年度数据
- 网址: https://data.stats.gov.cn/easyquery.htm?cn=E0105
- 路径: 首页 >> 地区数据 >> 主要城市年度数据
- 获取方式: 通过爬虫自动化获取

### 2. 补充数据源与补全说明

国家统计局数据存在部分缺失，通过以下渠道补全：

- **中国统计信息网** (http://www.tjcn.org/tjgb/) - 各地统计公报
- **城市政府官网** - 统计局公开数据
- **统计年鉴下载网** (https://web.xiaze.org/tjgb/) - 历年统计公报

使用Python爬虫从统计公报网站自动提取数据，若**爬取失败，则应用人工查询数据**。具体方法详见[01_data_clean](01_data_clean.ipynb);代码详见: [scrape_missing_data](codes/scrape_missing_data.py)

## （二）数据规范

清洗后的数据`city_budget_clean.csv`（GDP等数据）和`real_estate_clean.csv`（房地产相关数据）包含以下指标：

- `city`: 城市名称（36个主要城市）
- `year`: 年度（2006-2024）
- `income`: 地方一般公共预算收入(亿元)
- `expend`: 地方一般公共预算支出(亿元)
- `gdp`: 地区生产总值(亿元)
- `deposit`: 住户存款余额(亿元)
- `gap`: **预算缺口** = expend - income (亿元)
- `gap_to_gdp`: **预算缺口占GDP比重** = gap / gdp
- `income_growth`: 财政收入年度增长率(%)
- `expend_growth`: 财政支出年度增长率(%)
- `region_group`: 区域分组（珠三角/长三角/其他）
- `is_tier1`: 是否为一线城市（北上广深）
- `re_invest`:房地产开发投资额（亿元）
- `sale_area`:商品房销售面积（万平方米）
- `re_avg_price`:商品房平均销售价格（元/平方米）
- `res_sale_area`:住宅商品房销售面积（万平方米）
- `res_avg_price`:住宅商品房平均销售价格（元/平方米）

**详见**：https://github.com/Mineyme/25MDETeam01/blob/main/data_clean/city_all_clean.csv

## （三）质量说明

- **数据完整性**: 经补全后，所有核心指标(income, expend, gdp)无缺失
- **数据准确性**: 所有补全数据均来自官方统计公报，经人工核验
- **数据时效性**: 覆盖2006-2024年，共19年数据

## （四）注意事项

1. 房地产数据中拉萨市缺失较多（18-19个年份），分析时需注意
2. 增长率数据中每个城市2006年（第一年）无法计算，为正常缺失
3. 部分城市2024年数据可能为初步核算数据，后续可能调整

---

# 四、分析内容

## 1. 数据清洗 ([01_data_clean.ipynb](01_data_clean.ipynb))

- 数据获取与合并
- 缺失值处理与补全
- 计算衍生指标（gap, gap_to_gdp, 增长率）
- 城市分组标注

## 2. EDA分析 ([02_Fiscal_Gap_Profile_Analysis.ipynb](02_Fiscal_Gap_Profile_Analysis.ipynb))

- **特定年份gap_to_gdp极值城市**（2006, 2010, 2014, 2018, 2022）
- **北上广深财政对比**：gap_to_gdp、预算缺口、收支增长率
- **珠三角 vs 长三角**：区域财政差异分析
- **全国趋势**：gap_to_gdp分布与时序演变
- **收支增长率分析**：财政收支增速对比

## 3. 主题分析（T1-T5）

### T1：一线城市财政对比分析 ([03_T1_city_gap_to_GDP_analysis.ipynb](03_T1_city_gap_to_GDP_analysis.ipynb))


**分析范围：** 北京、上海、广州、深圳

**分析内容：**
1. **gap_to_gdp对比**
   - 深圳：平均3.04%（最优，经济强劲，收入充足）
   - 上海：平均3.2%（良好，长三角龙头）
   - 北京：平均3.5%（适中，全国政治中心）
   - 广州：平均4.05%（最高，财政压力相对较大）

2. **收支增长率对比**
   - 四城市收入增长速度对比（2006-2022年）
   - 支出增长的刚性特征对比分析
   - 经济周期对各城市的影响程度

3. **时序趋势分析**
   - 2009年金融危机对一线城市的影响
   - 2020年疫情前后财政变化
   - 长期可持续性评估

**主要结论：**
- 一线城市中深圳、上海财政状况最优，广州、北京面临相对较大的财政压力
- 深圳经济活力最强，财政自给能力最强
- 广州作为传统贸易中心，面临产业升级下的财政压力

---

### T2：区域财政差异分析 ([03_T2_region_gap_to_GDP_analysis.ipynb](03_T2_region_gap_to_GDP_analysis.ipynb))


**分析范围：** 珠三角 vs 长三角 vs 其他地区

**分析内容：**
1. **区域平均指标对比**
   - 珠三角平均gap_to_gdp：3.54%（压力较大）
   - 长三角平均gap_to_gdp：2.58%（压力较小）
   - 其他地区：4.2%+（压力最大）

2. **区域内部结构分析**
   - 珠三角内部差异：深圳、广州等领先城市与中山、江门等的对比
   - 长三角内部差异：发展相对均衡，二三线城市表现稳定
   - 城市分化的驱动因素

3. **时序演变分析（2006-2022）**
   - 两个区域缺口的长期趋势
   - 区域收支增长率对比
   - 经济周期影响的地区差异

**主要结论：**
- 长三角财政状况整体优于珠三角，生存期达 0.96pt
- 长三角内部城市发展更为均衡，不存在明显两极分化
- 珠三角作为改革开放前沿，面临产业升级和财政结构调整
- 长期看，长三角区域协调机制更完善，财政韧性更强

---

### T3：财政与房地产关系分析 ([03_T3_fiscal_real_estate_analysis.ipynb](03_T3_fiscal_real_estate_analysis.ipynb))


**分析内容：**
1. **房地产投资与财政缺口的关系**
   - 房地产投资/GDP与gap_to_gdp呈**负相关**（r = -0.38）
   - 房地产市场活跃的城市财政压力相对较小
   - 房地产收入对地方财政贡献度分析

2. **房价变化与财政的互动**
   - 房价上升对地方税收的正面影响
   - 房价下跌对财政收入的冲击程度
   - 2015年调整与2021年恢复的财政响应

3. **珠三角 vs 长三角房地产对比**
   - 珠三角：房价波动大，财政风险相对高
   - 长三角：房地产市场相对稳定，财政支撑作用更可持续
   - 土地财政依赖度分析

**主要结论：**
- 房地产市场活跃程度直接影响地方财政健康度
- 房价稳定增长的地区财政压力相对较小
- 房地产泡沫风险较高的城市应警惕财政风险

---

### T4：房地产投资与预算缺口分析 ([03_T4_re_invest_gap_to_GDP_analysis.ipynb](03_T4_re_invest_gap_to_GDP_analysis.ipynb))


**分析内容：**
1. **房地产投资规模与财政的关系**
   - 各城市房地产投资规模及年度增长
   - 投资高峰期（2009-2015年）与低谷期比较
   - 投资与土地出让收入的强相关性

2. **历次经济冲击的影响**
   - **2008年金融危机**：房地产投资下滑，财政缺口上升
   - **2015年房地产调整**：投资增速下降，部分城市财政压力加大
   - **2020年疫情冲击**：投资短期下滑，但快速恢复
   - **2021-2024年恢复**：投资增速放缓，但整体仍保持正增长

3. **投资与财政的互动机制**
   - 房地产投资驱动的地方税收增长
   - 投资下滑时的财政可持续性问题
   - 投资挤出效应分析

**主要结论：**
- 房地产投资与财政收入显著相关，房地产市场的波动对地方财政产生重要影响
- 过度依赖房地产投资的城市财政风险较高
- 需要推动产业多元化，降低对房地产的依赖

---

### T5：财政储蓄与预算缺口分析 ([03_T5_fiscal_savings_gap_analysis.ipynb](03_T5_fiscal_savings_gap_analysis.ipynb))


**分析内容：**
1. **居民储蓄与财政的关联**
   - 住户存款与地方财政收入的相关性分析
   - 高储蓄城市的财政风险评估
   - 存款增长与财政支出的对应性

2. **储蓄水平差异的含义**
   - 城市间储蓄差异与财政状况的关系
   - 储蓄率高的城市财政是否更健康
   - 城市发展阶段与储蓄模式

3. **财政应急能力评估**
   - 应急储蓄能力分析
   - 财政可持续性预测
   - 风险预警指标体系

**主要结论：**
- 高储蓄城市通常具备更强的财政韧性和应急能力
- 居民储蓄充分的城市在经济下行期间财政压力更小
- 长期看，应鼓励合理的居民储蓄积累，作为经济波动的缓冲

---

# 四、主要发现

### 预算缺口特征

- **2022年全国均值**: gap_to_gdp = 0.0608 (6.08%)
- **最大**: 拉萨 0.3784 (37.84%)
- **最小**: 杭州 0.0049 (0.49%)
- **北上广深**: 0.0304-0.0405之间，深圳最低(3.04%)，广州最高(4.05%)

### 区域差异

- **珠三角平均**: 0.0354 (3.54%)
- **长三角平均**: 0.0258 (2.58%)
- 长三角财政状况整体优于珠三角

### 房地产影响

- 房地产投资/GDP与gap_to_gdp呈**负相关**(-0.38)
- 房地产市场活跃的城市财政压力相对较小

---

# 五、项目结构

```
City_Budget_Analysis/
├── codes/                          # 辅助脚本
│   ├── fetch_data.py              # 数据获取（国家统计局API）
│   ├── scrape_missing_data.py     # 缺失数据爬虫（统计公报）
│   ├── fill_missing_data.py       # 数据补全与整合
│   ├── run_clean.py               # 数据清洗执行
│   ├── run_eda.py                 # EDA分析执行
│   └── run_re_analysis.py         # 房地产分析执行
├── data_raw/                       # 原始数据
│   ├── city_income.xlsx           # 财政收入
│   ├── city_expenditure.xlsx      # 财政支出
│   ├── individual_deposit.xlsx    # 储蓄存款
│   ├── gdp.xlsx                   # GDP
│   ├── re_*.xlsx                  # 房地产数据(5个文件)
│   ├── merged_raw.csv             # 合并原始数据
│   ├── merged_raw_filled.csv      # 补全后原始数据
│   ├── real_estate_raw.csv        # 房地产原始数据
│   └── missing_data_scraped.json  # 爬取的缺失数据
├── data_clean/                     # 清洗后数据
│   ├── city_budget_clean.csv      # 财政数据（清洗后）
│   ├── real_estate_clean.csv      # 房地产数据（清洗后）
│   └── city_all_clean.csv         # 完整合并数据
├── output/                         # 输出图表
│   ├── gap_to_gdp_extremes.xlsx/.png
│   ├── tier1_comparison.png
│   ├── pearl_vs_yangtze.png
│   ├── gap_to_gdp_distribution.png
│   ├── growth_rate_analysis.png
│   ├── gap_to_gdp_ranking_2022.png
│   ├── real_estate_gap_analysis.png
│   ├── pearl_yangtze_real_estate.png
│   └── real_estate_time_series.png
├── analysis_visual_report_html/           # 分析可视化HTML报告
│   ├── 02_Fiscal_Gap_Profile_Analysis.html
│   ├── 03_T1_city_gap_to_GDP_analysis.html
│   ├── 03_T2_region_gap_to_GDP_analysis.html
│   ├── 03_T3_fiscal_real_estate_analysis.html
│   ├── 03_T4_re_invest_gap_to_GDP_analysis.html
│   └── 03_T5_fiscal_savings_gap_analysis.html
├── README.md                       # 项目说明文档
├── 01_data_clean.ipynb            # 数据清洗笔记本
├── 02_Fiscal_Gap_Profile_Analysis.ipynb # 财政缺口分析笔记本
├── 03_T1_city_gap_to_GDP_analysis.ipynb # 一线城市分析
├── 03_T2_region_gap_to_GDP_analysis.ipynb # 区域对比分析
├── 03_T3_fiscal_real_estate_analysis.ipynb # 房地产分析
├── 03_T4_re_invest_gap_to_GDP_analysis.ipynb # 投资分析
└── 03_T5_fiscal_savings_gap_analysis.ipynb # 储蓄分析
```

---

# 六、技术栈和复现说明

## （一）技术栈

本项目主要使用以下Python库：

- **BeautifulSoup**：爬虫，用于原始数据获取。
- **pandas**：核心数据处理库，用于读取Excel、合并表格、清洗缺失值、分组聚合计算、数据重塁等。
- **numpy**：提供数学运算（如对数、加权平均、离群值裁剪）。
- **matplotlib**：基础绘图库，用于绘制折线图、双纵轴图，并保存为PNG文件。
- **seaborn**：基于matplotlib的高级绘图库，用于绘制箱线图，直观展示分布。
- **re**：正则表达式库。
- **warnings**：过滤无关警告，保持输出整洁。

代码按照"原始数据提取 → 数据清洗 → 指标计算 → 分析任务"的顺序组织，每个步骤均有详细注释，确保可读性和可复现性。

## （二）复现说明

### 1. 数据获取

```bash
python codes/fetch_data.py
```

### 2. 数据分析

```bash
python codes/run_clean.py           # 数据清洗
python codes/run_eda.py             # EDA分析
python codes/run_re_analysis.py     # 房地产分析
```

或直接运行Jupyter Notebook:

```bash
jupyter notebook 01_data_clean.ipynb
jupyter notebook 02_Fiscal_Gap_Profile_Analysis.ipynb
jupyter notebook 03_T1_city_gap_to_GDP_analysis.ipynb
jupyter notebook 03_T2_region_gap_to_GDP_analysis.ipynb
jupyter notebook 03_T3_fiscal_real_estate_analysis.ipynb
jupyter notebook 03_T4_re_invest_gap_to_GDP_analysis.ipynb
jupyter notebook 03_T5_fiscal_savings_gap_analysis.ipynb
```

---

# 许可证

本项目数据来源于公开统计数据，仅供学术研究使用。

---

# 更新日志

- **2026-03-17**: 初始版本，完成数据获取、清洗和分析
- **2026-03-17**: 补全缺失数据，添加爬虫脚本，更新README
- **2026-03-19**: 补充分析说明，修正codes下各py文件的路径问题，修复`codes/fill_missing_data.py`的问题
- **2026-03-20**: pull组员全部的分析主题，综合合并，补充Readme
