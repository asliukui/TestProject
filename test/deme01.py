import pandas as pd

# 创建一个示例 DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

print(df)

print(df.iloc[0,1])