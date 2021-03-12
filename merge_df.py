import pandas as pd

dex_df = pd.read_csv("drebin_dexfile_analysis.csv")
manifest_df = pd.read_csv("drebin_manifest_analysis.csv")

df = pd.merge(dex_df, manifest_df, how="inner", on=["id"])

df["is_malicious"] = 1
df.to_csv("drebin_analysis.csv", index=False)
