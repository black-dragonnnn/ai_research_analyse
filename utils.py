import re
from config import stop_words
import pandas as pd

def classify_organization(org_name):
    org_name = str(org_name).lower()
    company_keywords = ["google", "microsoft", "meta", "deepmind", "amazon", "baidu", "tencent"]
    if any(k in org_name for k in company_keywords):
        return "大型科技企业"
    elif any(word in org_name for word in ["university", "institute", "college"]):
        return "高校/科研院所"
    else:
        return "其他机构"

def clean_title(Title):
    """清洗标题：小写、清除符号、分词、过滤停用词"""
    Title = str(Title).lower()
    # 匹配所有非小写字母,非空格的字符，替换为空格
    Title = re.sub(r'[^a-z\s]', ' ', Title)
    words = Title.split()
    # 过滤停用词、长度小于3的无意义短单词
    valid_words = [w for w in words if w not in stop_words and len(w) >= 3]
    return valid_words     



