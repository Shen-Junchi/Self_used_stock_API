# Self_used_stock_API
This is an api used to get finance data in A stock 

```
import os
import sys
import pandas as pd
import numpy as np 
# 获取当前工作目录
current_dir = os.getcwd()
# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # 如果需要上一级目录

sys.path.insert(0, project_root)

# 导入模块
from self_package import get_stock
from self_package import tech_index as ti

# 使用函数
df_ts = get_stock.get_stock_data("601111", "daily", "20000101", "20250407")
df_ts = get_stock.standardize_stock_data(df_ts)

MA_5 = ti.MA(df_ts,'Open', 5)
MA_10 = ti.MA(df_ts,'Open', 10)
MA_20 = ti.MA(df_ts,'Open', 20)

nature_log_5_10 = ti.nature_log(MA_5, MA_10)
nature_log_5_20 = ti.nature_log(MA_5, MA_20)
nature_log_10_20 = ti.nature_log(MA_10, MA_20)

w = 0.01

# 创建一个新的 DataFrame 来存储结果
Fuzzification_10_20 = pd.DataFrame(columns=['Fuzzification_10_20'], index=nature_log_10_20.index)
Fuzzification_5_10 = pd.DataFrame(columns=['Fuzzification_5_10'], index=nature_log_5_10.index)
Fuzzification_5_20 = pd.DataFrame(columns=['Fuzzification_5_20'], index=nature_log_5_20.index)

# 遍历并只处理非 NaN 值
for idx in nature_log_10_20.index:
    value = nature_log_10_20.loc[idx]
    if not pd.isna(value) and value != 0:  # 检查是否为 NaN 或 0
        # 直接存储整个字典
        Fuzzification_10_20.at[idx, 'Fuzzification_10_20'] = ti.Fuzzification(value, w)
    else:
        # 对于 NaN 或零值，设置为 NaN
        Fuzzification_10_20.at[idx, 'Fuzzification_10_20'] = np.nan


for idx in nature_log_5_10.index:
    value = nature_log_5_10.loc[idx]
    if not pd.isna(value) and value != 0:  # 检查是否为 NaN 或 0
        # 直接存储整个字典
        Fuzzification_5_10.at[idx, 'Fuzzification_5_10'] = ti.Fuzzification(value, w)
    else:
        # 对于 NaN 或零值，设置为 NaN
        Fuzzification_5_10.at[idx, 'Fuzzification_5_10'] = np.nan

for idx in nature_log_5_20.index:   
    value = nature_log_5_20.loc[idx]
    if not pd.isna(value) and value != 0:  # 检查是否为 NaN 或 0
        # 直接存储整个字典
        Fuzzification_5_20.at[idx, 'Fuzzification_5_20'] = ti.Fuzzification(value, w)
    else:
        # 对于 NaN 或零值，设置为 NaN
        Fuzzification_5_20.at[idx, 'Fuzzification_5_20'] = np.nan


for dict in Fuzzification_5_10['Fuzzification_5_10']:
    activated_rules_1 = dict
    print(f"For fuzzified_input_1: {dict}")
    print(f"Activated output sets and strengths: {activated_rules_1}")


```
