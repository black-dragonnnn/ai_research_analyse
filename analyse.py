import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter

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


# --- 统计每年的论文数量 ---
year_count = data_new["Year"].value_counts().sort_index()
print(year_count)
print(type(year_count))
plt.figure(figsize=(10,5)) 
plt.plot(year_count.index, year_count.values)
plt.xlabel("年份")
plt.ylabel("论文数量")
plt.title("三大会议历年论文数量")
plt.xticks(range(int(year_count.index.min()), int(year_count.index.max()) + 1))
ax = plt.gca()
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: str(int(x))))
plt.show()  

# --- 历年高校与科技企业论文产出对比 ---
def classify_organization(org_name):
    org_name = str(org_name).lower()
    company_keywords = ["google", "microsoft", "meta", "deepmind", "amazon", "baidu", "tencent"]
    if any(k in org_name for k in company_keywords):
        return "大型科技企业"
    elif any(word in org_name for word in ["university", "institute", "college"]):
        return "高校/科研院所"
    else:
        return "其他机构"

# 新增分类标签
data_new["机构类型"] = data_new["Affiliation"].apply(classify_organization)

# 按年份 + 机构类型聚合统计
year_Affi_df = data_new.groupby(["Year", "机构类型"]).size().unstack()
print(year_Affi_df)

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
plt.show()



# --- 统计热词 ---
# 停用词（过滤无意义虚词，可自行扩充）
stop_words = {
    'the', 'of', 'and', 'a', 'in', 'for', 'on', 'with', 'to', 'is', 'are', 
    'an', 'by', 'from', 'as', 'at', 'be', 'this', 'that', 'it', 'its',
    'we', 'our', 'can', 'has', 'have', 'not', 'or', 'but', 'than', 'more',
    'based', 'using', 'via', 'towards', 'into', 'over', 'under', 'new',
    'toward', 'about', 'between', 'among', 'which', 'all', 'each', 'some','learning'
}

def clean_title(Title):
    """清洗标题：小写、清除符号、分词、过滤停用词"""
    Title = str(Title).lower()
    # 匹配所有非小写字母,非空格的字符，替换为空格
    Title = re.sub(r'[^a-z\s]', ' ', Title)
    words = Title.split()
    # 过滤停用词、长度小于3的无意义短单词
    valid_words = [w for w in words if w not in stop_words and len(w) >= 3]
    return valid_words

# 统计热词
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
plt.show()  