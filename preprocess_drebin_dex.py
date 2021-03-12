import pandas as pd

all_df = pd.DataFrame()
for i in range(1, 7):
    df = pd.read_csv("./drebin_dexfile_analysis_" +
                     str(i) + ".csv", index_col=0)
    all_df = pd.concat([all_df, df])

print(all_df)
# all_df = all_df.rename(columns={1: "id"}, inplace=True)
all_df.to_csv(
    "drebin_dexfile_analysis.csv", index=False)
