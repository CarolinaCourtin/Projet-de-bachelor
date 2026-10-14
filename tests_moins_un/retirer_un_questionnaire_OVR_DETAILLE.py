import json
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


X = []
Y = []

with open('complete_detailed_data_questionnaires_TEST.json', 'r') as f:
    data = json.load(f)

    for questionnaire in data.values():

        # -------------- remplissage de X -------------------------

        new_questionnaire_X = []

        X.append(new_questionnaire_X)

        paire_de_mot_values = []

        new_questionnaire_X.append(paire_de_mot_values)

        # ajout des données de paire de mots

        QP_values = []

        paire_de_mot_values.append(QP_values)

        for QP_value in questionnaire['paire_de_mots']['QP'].values():
            QP_values.append(QP_value)

        QHS_values = []

        paire_de_mot_values.append(QHS_values)

        for QHS_value in questionnaire['paire_de_mots']['QHS'].values():
            QHS_values.append(QHS_value)

        QHI_values = []

        paire_de_mot_values.append(QHI_values)

        for QHI_value in questionnaire['paire_de_mots']['QHI'].values():
            QHI_values.append(QHI_value)

        ATT_values = []

        paire_de_mot_values.append(ATT_values)

        for ATT_value in questionnaire['paire_de_mots']['ATT'].values():
            ATT_values.append(ATT_value)

        new_questionnaire_Y = []

        Y.append(new_questionnaire_Y)

        for probleme in questionnaire['probleme']:
            problems_values = []

            new_questionnaire_Y.append(problems_values)

            problems_values.append(probleme)

np.set_printoptions(precision=4, suppress=True)

X_flattened = []

for sample in X:

    flattened_sample = []
    for category in sample[0]:
        flattened_sample.extend(category)
    X_flattened.append(flattened_sample)

X_flattened = np.array(X_flattened)

# print(f"Nouveau X flattened : {X_flattened}\n")

# MATRICE Y

formatted_labels = [[label[0] for label in sample] for sample in Y]

mlb = MultiLabelBinarizer()

Y_binary_labels = mlb.fit_transform(formatted_labels)

# print(f"Nouveau Y matriciel : {Y_binary_labels}\n")

# noms de chaque colonne
column_names = mlb.classes_

# print(f"Colonnes : {column_names}\n")

# instance de LOOCV
cv = LeaveOneOut()


# modèle ML à utiliser
base_lr = KNeighborsClassifier()

for i in range(X_flattened.shape[0]):

    y_true, y_pred = list(), list()

    X_train_deleted = np.delete(X_flattened, i, axis=0)
    y_train_deleted = np.delete(Y_binary_labels, i, axis=0)

    print(f"Valeur retirée : {X_flattened[i].reshape(1, -1)}")

    # X_test = X_flattened[i].reshape(1, -1)
    # y_test = Y_binary_labels[i].reshape(1, -1)

    for train_ix, test_ix in cv.split(X_train_deleted):

        X_train, X_test = X_train_deleted[train_ix, :], X_train_deleted[test_ix, :]

        y_train, y_test = y_train_deleted[train_ix], y_train_deleted[test_ix]

        # Initialiser et entraîner ClassifierChain
        ovr = OneVsRestClassifier(base_lr)
        ovr.fit(X_train, y_train)

        # Prédire pour l'exemple de test
        y_pred_single = ovr.predict(X_test)

        print(f"Prediction : {y_pred_single}")
        print(f"Valeur exacte : {y_test}")

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

    print(f"Label-based accuracy : {label_based_accuracy:.4f}")