# Self_used_stock_API
This is an api used to get finance data in A stock 

```
from get_stock import get_stock_data
from get_stock import standardize_stock_data

# 获取当前工作目录
current_dir = os.getcwd()

# 将项目根目录添加到 Python 路径
project_root = os.path.abspath(os.path.join(current_dir, ".."))  # 如果需要上一级目录
sys.path.insert(0, project_root)

# 导入模块
from self_package import get_stock

df_ts = get_stock_data("601111", "daily", "20000101", "20250407")
df_ts = standardize_stock_data(df_ts)
```
