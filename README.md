ex_Team01 中国主要城市公共预算支出和收入数据分析
---
# 一、作业说明
**选题**：T2 - 中国主要城市公共预算支出和收入数据分析
**班级**：25MDE PC
**组号**：G1
**组员**：钟梅（组长）、王海林、王晓航、吴惠彪、梁小婵、梁佩文、章翔宇、曾铮
**日期**：2026年3月19日

# 二、项目概述
本项目对中国36个主要城市2006-2024年的财政收支、GDP和房地产数据进行系统分析，重点研究预算缺口(gap)及其占GDP比重(gap_to_gdp)的地区差异和时序特征。

# 三、数据说明
## （一）数据来源
### 1.主要数据源
- **国家统计局** - 主要城市年度数据
  - 网址: https://data.stats.gov.cn/easyquery.htm?cn=E0105
  - 路径: 首页 >> 地区数据 >> 主要城市年度数据
  - 获取方式: 通过爬虫自动化获取

### 2.补充数据源与补全说明
国家统计局数据存在部分缺失，通过以下渠道补全：
- **中国统计信息网** (http://www.tjcn.org/tjgb/) - 各地统计公报
- **城市政府官网** - 统计局公开数据
- **统计年鉴下载网** (https://web.xiaze.org/tjgb/) - 历年统计公报

使用Python爬虫从统计公报网站自动提取数据，若**爬取失败，则应用人工查询数据**。
具体方法详见[01_data_clean](01_data_clean.ipynb);代码详见: [scrape_missing_data](codes/scrape_missing_data.py)

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
## （三）质量说明
- **数据完整性**: 经补全后，所有核心指标(income, expend, gdp)无缺失
- **数据准确性**: 所有补全数据均来自官方统计公报，经人工核验
- **数据时效性**: 覆盖2006-2024年，共19年数据
## （四）注意事项
1. 房地产数据中拉萨市缺失较多（18-19个年份），分析时需注意
2. 增长率数据中每个城市2006年（第一年）无法计算，为正常缺失
3. 部分城市2024年数据可能为初步核算数据，后续可能调整

# 四、分析内容
## 1. 数据清洗 (`01_data_clean.ipynb`)
- 数据获取与合并
- 缺失值处理与补全
- 计算衍生指标（gap, gap_to_gdp, 增长率）
- 城市分组标注

## 2. EDA分析 (`02_EDA_analysis.ipynb`)
- **特定年份gap_to_gdp极值城市**（2006, 2010, 2014, 2018, 2022）
- **北上广深财政对比**：gap_to_gdp、预算缺口、收支增长率
- **珠三角 vs 长三角**：区域财政差异分析
- **全国趋势**：gap_to_gdp分布与时序演变
- **收支增长率分析**：财政收支增速对比

## 3. 房地产分析 (`03_real_estate_analysis.ipynb`)
- **房地产投资与预算缺口关系**
- **珠三角 vs 长三角房地产对比**
- **房地产市场变化的时序特征**
- **房价、销售与财政缺口的相关性分析**

# 四、主要发现
-[ ] 要改成全局性、概括性的话
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
├── README.md                       # 项目说明文档
├── 01_data_clean.ipynb            # 数据清洗笔记本
├── 02_EDA_analysis.ipynb          # EDA分析笔记本
└── 03_real_estate_analysis.ipynb  # 房地产分析笔记本
```

## （一）技术栈
本项目主要使用以下Python库：
- **BeautifulSoup**：爬虫，用于原始数据获取。
- **pandas**：核心数据处理库，用于读取Excel、合并表格、清洗缺失值、分组聚合计算、数据重塑等。
- **numpy**：提供数学运算（如对数、加权平均、离群值裁剪）。
- **matplotlib**：基础绘图库，用于绘制折线图、双纵轴图，并保存为PNG文件。
- **seaborn**：基于matplotlib的高级绘图库，用于绘制箱线图，直观展示分布。
- **re**：正则表达式库。
- **warnings**：过滤无关警告，保持输出整洁。
代码按照“原始数据提取 → 数据清洗 → 指标计算 → 分析任务”的顺序组织，每个步骤均有详细注释，确保可读性和可复现性。

## （二）复现说明

### 1. 数据获取
```bash
python codes/raw_data_get.py
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
jupyter notebook 02_EDA_analysis.ipynb
jupyter notebook 03_real_estate_analysis.ipynb
```

# 许可证
本项目数据来源于公开统计数据，仅供学术研究使用。

# 更新日志
- 2026-03-17: 初始版本，完成数据获取、清洗和分析
- 2026-03-17: 补全缺失数据，添加爬虫脚本，更新README
- 2026-03-19：补充分析说明，修正codes下各py文件的路径问题，修复`codes/fill_missing_data.py`的问题
