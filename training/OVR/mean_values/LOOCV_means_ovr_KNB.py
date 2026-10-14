from sklearn.model_selection import LeaveOneOut
import json
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

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

# APPLATISSEMENT DES DONNEES

X_flattened = np.array(X)
# print(X_flattened)

# MATRICE Y

# Transformation des étiquettes en une liste de listes de chaînes de caractères
formatted_labels = [[label for label in sample] for sample in Y]

mlb = MultiLabelBinarizer()

Y_binary_labels = mlb.fit_transform(formatted_labels)

# print(f"Nouveau Y matriciel : {Y_binary_labels}\n")

column_names = mlb.classes_

print(f"Colonnes : {column_names}\n")

cv = LeaveOneOut()

y_true, y_pred = list(), list()

base_lr = KNeighborsClassifier()

for train_ix, test_ix in cv.split(X_flattened):

    X_train, X_test = X_flattened[train_ix, :], X_flattened[test_ix, :]

    print(f"X train : {X_train}")
    print(f"X test : {X_test}")

    y_train, y_test = Y_binary_labels[train_ix], Y_binary_labels[test_ix]

    print(f"Y train : {y_train}")
    print(f"Ytest : {y_test}")

    # Initialiser et entraîner Ovr
    ovr = OneVsRestClassifier(base_lr)
    ovr.fit(X_train, y_train)

    # Prédire pour l'exemple de test
    y_pred_single = ovr.predict(X_test)

    print(f"prediction single {y_pred_single}")

    # Stocker les vraies valeurs et les prédictions
    y_true.append(y_test[0])
    y_pred.append(y_pred_single[0])

y_true = np.array(y_true)
y_pred = np.array(y_pred)

print(f"y_true : \n {y_true}")
print(f"y_pred : \n {y_pred}")


exact_accuracy = accuracy_score(y_true, y_pred)
print(f"Exact match ratio accuracy : {exact_accuracy:.4f}")


label_accuracies = [accuracy_score(y_true[:, i], y_pred[:, i]) for i in range(y_true.shape[1])]
label_based_accuracy = np.mean(label_accuracies)

print(f"Label-based accuracy: {label_based_accuracy:.4f}")