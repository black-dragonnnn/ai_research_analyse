# 停用词（过滤无意义虚词，可自行扩充）
stop_words = {
    'the', 'of', 'and', 'a', 'in', 'for', 'on', 'with', 'to', 'is', 'are', 
    'an', 'by', 'from', 'as', 'at', 'be', 'this', 'that', 'it', 'its',
    'we', 'our', 'can', 'has', 'have', 'not', 'or', 'but', 'than', 'more',
    'based', 'using', 'via', 'towards', 'into', 'over', 'under', 'new',
    'toward', 'about', 'between', 'among', 'which', 'all', 'each', 'some','learning'
}

# 数据库MySQL配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",       
    "password": "123777",
    "database": "paper_analysis",
    "charset": "utf8mb4"
}

#分辨率参数
DPI = 300

