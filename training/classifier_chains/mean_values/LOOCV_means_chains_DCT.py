from sklearn.model_selection import LeaveOneOut
import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multioutput import ClassifierChain
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

X = []
Y = []

with open('../../../questionnaires/mean_values_questionnaires.json', 'r') as f:
    data = json.load(f)
    for questionnaire in data.values():
        # -------------- remplissage de X -------------------------
        new_questionnaire_X = []
        X.append(new_questionnaire_X)
        for mean_value in questionnaire['valeurs_moyennes'].values():
            new_questionnaire_X.append(mean_value)

        # ------------- remplissage de Y -------------------------------------

        new_questionnaire_Y = []
        Y.append(new_questionnaire_Y)
        for probleme in questionnaire['probleme']:
            new_questionnaire_Y.append(probleme)

X_flattened = np.array(X)

formatted_labels = [[label for label in sample] for sample in Y]
mlb = MultiLabelBinarizer()
Y_binary_labels = mlb.fit_transform(formatted_labels)

cv = LeaveOneOut()

y_true, y_pred = list(), list()

base_lr = DecisionTreeClassifier()

for train_ix, test_ix in cv.split(X_flattened):
    X_train, X_test = X_flattened[train_ix], X_flattened[test_ix]
    y_train, y_test = Y_binary_labels[train_ix], Y_binary_labels[test_ix]

    chain = ClassifierChain(base_estimator=base_lr, order='random', random_state=42)
    chain.fit(X_train, y_train)

    y_pred_single = chain.predict(X_test)

    y_true.append(y_test[0])
    y_pred.append(y_pred_single[0])

y_true = np.array(y_true)
y_pred = np.array(y_pred)

accuracy = accuracy_score(y_true, y_pred)
print(f"Exact match ratio : {accuracy}")

label_accuracies = [accuracy_score(y_true[:, i], y_pred[:, i]) for i in range(y_true.shape[1])]
label_based_accuracy = np.mean(label_accuracies)

print(f"Label-based accuracy : {label_based_accuracy:.4f}")
