import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

df1 = pd.read_csv("datasets/androzoo_dexfile_analysis.csv")
df1["is_malicious"] = 0
df2 = pd.read_csv("datasets/drebin_dexfile_analysis.csv")
df2["is_malicious"] = 1

df = pd.concat([df1, df2])

df.to_csv("dex_dataset.csv")

X = df.drop(["id", "is_malicious"], axis=1)
y = df["is_malicious"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1)

# scaler = StandardScaler()
# scaler.fit(X_train)

# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)

# rf_clf = RandomForestClassifier()
# rf_clf.fit(X_train, y_train)

# rf_y_pred = rf_clf.predict(X_test)
# acc = accuracy_score(y_test, rf_y_pred)
# f1 = f1_score(y_test, rf_y_pred)
# recall = recall_score(y_test, rf_y_pred)
# precision = precision_score(y_test, rf_y_pred)

# print(acc)
# print(f1)
# print(recall)
# print(precision)
