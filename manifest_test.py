import pandas as pd
from operator import or_

df = pd.read_csv("./malicious_dataframe.csv")

arr = df.to_numpy()
col_sum = [i for i, v in enumerate(arr.sum(axis=0)) if v == 0]
# print(len(col_sum))

list_column = list(df)
# print(list_column)

delete_col_list = [v for i, v in enumerate(list_column) if i in col_sum]
# print(delete_col_list)

new_df = df.drop(delete_col_list, axis=1)
new_df.to_csv("processed_malicious_manifest.csv")
