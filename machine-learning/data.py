from sklearn.model_selection import train_test_split
import pandas as pd

# Read dataset
df = pd.read_csv("processed_manifest.csv")

# Extract Features and Labels
X = df.drop(["idx", "id", "is_malicious"], axis=1)  # Features
y = df["is_malicious"]  # Label

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1)
