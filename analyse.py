import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from collections import Counter
from utils import classify_organization, clean_title
import config

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 解决中文乱码
plt.rcParams["axes.unicode_minus"] = False

# 读取csv
data = pd.read_csv("papers.csv")
print(f"表头:{data.columns.tolist()}")
print(f"原始总条数:{len(data)}")

# 清洗：剔除column为Affiliation的无效数据
data_new = data.copy()
# 1. 去除column为Affiliation的值首尾空格
data_new["Affiliation"] = data_new["Affiliation"].str.strip()
# 2. 去除column为Affiliation的值为NaN的行
data_new = data_new[data_new["Affiliation"].notna()]
print(f"清洗后有效数据:{len(data_new)}")

# 写入mysql
engine = create_engine("mysql+pymysql://root:123777@localhost:3306/paper_analysis?charset=utf8mb4")
data_new.to_sql(
    name="papers_clean",   
    con=engine,           
    if_exists="replace",    
    index=False             # 不要把pandas自动索引存进数据库
)

# --- 统计每年的论文数量 ---
year_count = data_new["Year"].value_counts().sort_index()
print(year_count)
#写入mysql
year_count.to_sql(
    name="papers_year_count",    # MySQL里的表名
    con=engine,            
    if_exists="replace",   
    index=True          # 不要把pandas自动索引存进数据库
)
print(type(year_count))
plt.figure(figsize=(10,5)) 
plt.plot(year_count.index, year_count.values)
plt.xlabel("年份")
plt.ylabel("论文数量")
plt.title("三大会议历年论文数量")
plt.xticks(range(int(year_count.index.min()), int(year_count.index.max()) + 1))
ax = plt.gca()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: str(int(x))))
plt.savefig(fname="picture/历年论文数量.png", dpi=config.DPI, bbox_inches=None)
plt.show()  


# --- 历年高校与科技企业论文产出对比 ---
# 新增分类标签
data_new["机构类型"] = data_new["Affiliation"].apply(classify_organization)

# 按年份 + 机构类型聚合统计
year_Affi_df = data_new.groupby(["Year", "机构类型"]).size().unstack()
print(year_Affi_df)
#写入mysql
year_Affi_df.to_sql(
    name="papers_year_Affi",   
    con=engine,            
    if_exists="replace",   
    index=True        
)
print(type(year_Affi_df))
plt.figure(figsize=(10,5))
year_Affi_df.plot(ax=plt.gca())
plt.xlabel("年份")
plt.ylabel("论文数量")
plt.title("历年高校与科技企业论文产出对比")
plt.grid(alpha=0.3)
plt.legend()
# 设置x轴刻度为整数, 且显示所有年份
plt.xticks(range(int(year_Affi_df.index.min()), int(year_Affi_df.index.max()) + 1))
ax = plt.gca()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: str(int(x))))
plt.savefig(fname="picture/机构产出对比.png", dpi=config.DPI, bbox_inches=None)
plt.show()

# --- 统计热词 ---
all_words = []
for Title_text in data_new["Title"]:
    all_words.extend(clean_title(Title_text))

word_counter = Counter(all_words)
top_num = 20
top_words = word_counter.most_common(top_num)

# 控制台打印TOP热词
print(f"标题热词 Top {top_num}：")
for word, count in top_words:
    print(f"{word} : {count}")
#写入mysql
top_words_df = pd.DataFrame(top_words, columns=["热词", "出现频次"])
top_words_df.to_sql(
    name="papers_top_words",   
    con=engine,            
    if_exists="replace",   
    index=True        
)
print(type(top_words_df))
# 绘制横向柱状图 
words_index = [item[0] for item in top_words]
count_index = [item[1] for item in top_words]

plt.figure(figsize=(12, 7))
# 反转顺序，高频词显示在图表上方
plt.barh(words_index[::-1], count_index[::-1], color="#4372c4")
plt.xlabel("出现频次")
plt.ylabel("热词")
plt.title(f"论文标题 Top {top_num} 高频热词统计")
plt.tight_layout()
plt.savefig(fname="picture/top20热词.png", dpi=config.DPI, bbox_inches=None)
plt.show()  
