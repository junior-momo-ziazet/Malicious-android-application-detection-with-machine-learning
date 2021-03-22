from sklearn.metrics import confusion_matrix, classification_report


def create_report(filename, y_test, y_pred):
    with open(filename, mode="w") as f:
        # Confusion Matrix
        print("Confusion Matrix:", file=f)
        print("==================================================", file=f)
        print(confusion_matrix(y_test, y_pred), file=f)
        print("\n\n", file=f)

        # Classification Report
        print("Classification Report", file=f)
        print("==================================================", file=f)
        print(classification_report(y_test, y_pred), file=f)
