import pandas as pd

df = pd.read_csv("./datasets/drebin_manifest_analysis.csv")

del df["id"]

arr = df.to_numpy()

col_name = list(df.columns.values)

col_sum = arr.sum(axis=0)

my_arr = []

for idx, col in enumerate(col_sum):
    my_arr.append((col_name[idx], col_sum[idx]))

print(col_sum)
