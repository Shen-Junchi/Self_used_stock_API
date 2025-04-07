# Self_used_stock_API
This is an api used to get finance data in A stock 

```
from get_stock import get_stock_data
from get_stock import standardize_stock_data

df_ts = get_stock_data("601111", "daily", "20000101", "20250407")
df_ts = standardize_stock_data(df_ts)
```
