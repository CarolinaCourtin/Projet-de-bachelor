import json
import numpy as np
from sklearn.model_selection import train_test_split, LeaveOneOut
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

X = []
Y = []

with open('../../../questionnaires/complete_detailed_data_questionnaires.json', 'r') as f:

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
        # ------------- remplissage de Y -------------------------------------

        new_questionnaire_Y = []

        Y.append(new_questionnaire_Y)

        for probleme in questionnaire['probleme']:

            problems_values = []

            new_questionnaire_Y.append(problems_values)

            problems_values.append(probleme)

# APPLATISSEMENT DES DONNEES

np.set_printoptions(precision=4, suppress=True)

X_flattened = []
for sample in X:
    flattened_sample = []

    for category in sample[0]:
        flattened_sample.extend(category)

    X_flattened.append(flattened_sample)

X_flattened = np.array(X_flattened)

print(X_flattened)


# MATRICE Y

# Transformation des étiquettes en une liste de listes de chaînes de caractères
formatted_labels = [[label[0] for label in sample] for sample in Y]

# Création d'une instance de MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Adapter et transformer les étiquettes en une matrice binaire
Y_binary_labels = mlb.fit_transform(formatted_labels)

# Afficher la matrice binaire
print(f"Nouveau Y matriciel : {Y_binary_labels}\n")

# Obtenir les noms de chaque colonne
column_names = mlb.classes_

print(f"Colonnes : {column_names}\n")

cv = LeaveOneOut()

y_true, y_pred = list(), list()

base_lr = GaussianNB()

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