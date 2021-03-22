from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
from data import X_train, X_test, y_train, y_test
from create_report import create_report


# =================================================================
# ==================== MACHINE LEARNING MODELS ====================
# =================================================================


# ==================== Decision Tree Classifier ====================

dt_clf = DecisionTreeClassifier()
dt_clf.fit(X_train, y_train)

dt_y_pred = dt_clf.predict(X_test)

create_report("results/decision_tree_classifier_report2.txt",
              y_test, dt_y_pred)

dt_accuracy_score = accuracy_score(y_test, dt_y_pred)
dt_precision_score = precision_score(y_test, dt_y_pred)
dt_recall_score = recall_score(y_test, dt_y_pred)
dt_f1_score = f1_score(y_test, dt_y_pred)


# ==================== Random Forest Classifier ====================

rf_clf = RandomForestClassifier(n_estimators=4)
rf_clf.fit(X_train, y_train)

rf_y_pred = rf_clf.predict(X_test)

create_report("results/random_forest_classifier_report4.txt",
              y_test, rf_y_pred)

rf_accuracy_score = accuracy_score(y_test, rf_y_pred)
rf_precision_score = precision_score(y_test, rf_y_pred)
rf_recall_score = recall_score(y_test, rf_y_pred)
rf_f1_score = f1_score(y_test, rf_y_pred)


# ==================== KNN Classifier ====================

knn_clf = KNeighborsClassifier(n_neighbors=3)
knn_clf.fit(X_train, y_train)

knn_y_pred = knn_clf.predict(X_test)

create_report("results/knn_classifier_report3.txt", y_test, knn_y_pred)

knn_accuracy_score = accuracy_score(y_test, knn_y_pred)
knn_precision_score = precision_score(y_test, knn_y_pred)
knn_recall_score = recall_score(y_test, knn_y_pred)
knn_f1_score = f1_score(y_test, knn_y_pred)


# ==================== MLP Classifier ====================

mlp_clf = MLPClassifier(random_state=1)
mlp_clf.fit(X_train, y_train)

mlp_y_pred = mlp_clf.predict(X_test)

create_report("results/mlp_classifier_report3.txt", y_test, mlp_y_pred)

mlp_accuracy_score = accuracy_score(y_test, mlp_y_pred)
mlp_precision_score = precision_score(y_test, mlp_y_pred)
mlp_recall_score = recall_score(y_test, mlp_y_pred)
mlp_f1_score = f1_score(y_test, mlp_y_pred)


# ==================== SVC ====================

svc = SVC()
svc.fit(X_train, y_train)

svc_y_pred = svc.predict(X_test)

create_report("results/svc_report3.txt", y_test, svc_y_pred)

svc_accuracy_score = accuracy_score(y_test, svc_y_pred)
svc_precision_score = precision_score(y_test, svc_y_pred)
svc_recall_score = recall_score(y_test, svc_y_pred)
svc_f1_score = f1_score(y_test, svc_y_pred)


# ==================== Linear SVC ====================

linear_svc = LinearSVC(random_state=0)
linear_svc.fit(X_train, y_train)

linear_svc_y_pred = linear_svc.predict(X_test)

create_report("results/linear_svc_report3.txt", y_test, linear_svc_y_pred)

linear_svc_accuracy_score = accuracy_score(y_test, linear_svc_y_pred)
linear_svc_precision_score = precision_score(y_test, linear_svc_y_pred)
linear_svc_recall_score = recall_score(y_test, linear_svc_y_pred)
linear_svc_f1_score = f1_score(y_test, linear_svc_y_pred)


# # ==================== Gaussian Naive Bayes Classifier ====================

# gnb_clf = GaussianNB()
# gnb_clf.fit(X_train, y_train)

# gnb_y_pred = gnb_clf.predict(X_test)

# create_report("results/gaussian_nb_classifier_report3.txt", y_test, gnb_y_pred)

# gnb_accuracy_score = accuracy_score(y_test, gnb_y_pred)
# gnb_precision_score = precision_score(y_test, gnb_y_pred)
# gnb_recall_score = recall_score(y_test, gnb_y_pred)
# gnb_f1_score = f1_score(y_test, gnb_y_pred)


# # ==================== Multinomial Naive Bayes Classifier ====================

# mnb_clf = MultinomialNB()
# mnb_clf.fit(X_train, y_train)

# mnb_y_pred = mnb_clf.predict(X_test)

# create_report("results/multinomial_nb_classifier_report3.txt",
#               y_test, mnb_y_pred)

# mnb_accuracy_score = accuracy_score(y_test, mnb_y_pred)
# mnb_precision_score = precision_score(y_test, mnb_y_pred)
# mnb_recall_score = recall_score(y_test, mnb_y_pred)
# mnb_f1_score = f1_score(y_test, mnb_y_pred)


# =========================================================
# ==================== MODELS ANALYSIS ====================
# =========================================================


# ==================== Accuracy Analysis ====================

labels = ["DT", "RF", "KNN", "SVC", "Lin. SVC"]
accuracy_scores = [dt_accuracy_score, rf_accuracy_score, knn_accuracy_score,
                   svc_accuracy_score, linear_svc_accuracy_score]

plt.bar(labels, accuracy_scores, width=0.5)
plt.title = "Accuracy Score Comparison Between Different Models"
plt.xlabel = "Model"
plt.ylabel = "Accuracy Score"
plt.show()

# ==================== F1 Score Analysis ====================

f1_scores = [dt_f1_score, rf_f1_score, knn_f1_score,
             svc_f1_score, linear_svc_f1_score]

plt.bar(labels, f1_scores, width=0.5)
plt.title = "F1 Score Comparison Between Different Models"
plt.xlabel = "Model"
plt.ylabel = "F1 Score"
plt.show()
