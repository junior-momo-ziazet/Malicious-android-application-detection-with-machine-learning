import pandas as pd
import matplotlib.pyplot as plt

dreb_df = pd.read_csv("./datasets/drebin_manifest_analysis.csv")
dreb_df["is_malicious"] = 1

andro_df = pd.read_csv("./androzoo_manifest_analysis.csv")
andro_df["is_malicious"] = 0

merged_df = pd.concat([dreb_df, andro_df])

arr = merged_df.to_numpy()
col_sum = [i for i, v in enumerate(arr.sum(axis=0)) if v == 0]

list_column = list(merged_df)
# print(list_column)

delete_col_list = [v for i, v in enumerate(list_column) if i in col_sum]

new_df = merged_df.drop(delete_col_list, axis=1)
del new_df["id"]
df_arr = new_df.to_numpy()
col_name = list(new_df.columns.values)
df_col_sum = df_arr.sum(axis=0)
# print(df_col_sum)

new_dreb_df = dreb_df.drop(delete_col_list, axis=1)
del new_dreb_df["id"]
dreb_arr = new_dreb_df.to_numpy()
col_name = list(new_dreb_df.columns.values)
dreb_col_sum = dreb_arr.sum(axis=0)
# print(dreb_col_sum)

new_andro_df = andro_df.drop(delete_col_list, axis=1)
del new_andro_df["id"]
andro_arr = new_andro_df.to_numpy()
col_name = list(new_andro_df.columns.values)
andro_col_sum = andro_arr.sum(axis=0)
# print(andro_col_sum)

# plt.plot(dreb_col_sum)
# plt.plot(andro_col_sum)
# plt.plot(df_col_sum)
# plt.plot([new_df.shape[0] * 0.01 for i in range(len(df_col_sum))])
# plt.plot([new_df.shape[0] * 0.9 for i in range(len(df_col_sum))])
# # plt.show()

columns = [j for i, j in enumerate(
    list(new_df)) if df_col_sum[i] > 0.01 * new_df.shape[0]]

print(len(columns))
row_sum = df_arr.sum(axis=1)
print(row_sum)
plt.plot(row_sum)
plt.show()
# print(dreb_arr[4368])

# permission = list(new_andro_df)[df_col_sum[0:20].argmax()]
# print(permission)

# # new_df.to_csv("processed_manifest.csv")
# print(len(list(new_df.columns.values)))
