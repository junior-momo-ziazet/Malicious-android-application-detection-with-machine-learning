from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Read dataset
df = pd.read_csv("processed_manifest.csv")

# Extract Features and Labels
X = df.drop(["idx", "id", "is_malicious"], axis=1)  # Features
y = df["is_malicious"]  # Label

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1)

X_train = X_train.to_numpy()
X_test = X_test.to_numpy()

# scaler = StandardScaler()
# scaler.fit(X_train)

# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)

rf_clf = RandomForestClassifier()
rf_clf.fit(X_train, y_train)

rf_y_pred = rf_clf.predict(X_test)

feature_imp = [index for index, value in enumerate(list(
    rf_clf.feature_importances_)) if value != 0]

X_train = X_train[:, feature_imp]
X_test = X_test[:, feature_imp]

pca = PCA(n_components=20)
pca.fit(X_train)

X_train = pca.transform(X_train)
X_test = pca.transform(X_test)
