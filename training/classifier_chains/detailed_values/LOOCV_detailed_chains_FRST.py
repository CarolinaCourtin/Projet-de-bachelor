import json
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multioutput import ClassifierChain
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

X = []
Y = []

with open('../../../questionnaires/complete_detailed_data_without_mediaserver.json', 'r') as f:

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

# APPLATISSEMENT DES DONNEES X

print(X)

np.set_printoptions(precision=4, suppress=True)

X_flattened = []

for sample in X:

    flattened_sample = []
    for category in sample[0]:
        flattened_sample.extend(category)
    X_flattened.append(flattened_sample)

X_flattened = np.array(X_flattened)

print(f"Nouveau X flattened : {X_flattened}\n")

# MATRICE Y

formatted_labels = [[label[0] for label in sample] for sample in Y]

mlb = MultiLabelBinarizer()

Y_binary_labels = mlb.fit_transform(formatted_labels)

print(f"Nouveau Y matriciel : {Y_binary_labels}\n")

# noms de chaque colonne
column_names = mlb.classes_

print(f"Colonnes : {column_names}\n")

# instance de LOOCV
cv = LeaveOneOut()

# liste des données prédites et des vraies prédictions
y_true, y_pred = list(), list()

# modèle ML à utiliser
base_lr = RandomForestClassifier(random_state=42)

# Initialiser et entraîner ClassifierChain
chain = ClassifierChain(base_estimator=base_lr, order='random', random_state=85)

for train_ix, test_ix in cv.split(X_flattened):

    X_train, X_test = X_flattened[train_ix, :], X_flattened[test_ix, :]

    print(f"X train : {X_train}")
    print(f"X test : {X_test}")

    y_train, y_test = Y_binary_labels[train_ix], Y_binary_labels[test_ix]

    print(f"Y train : {y_train}")
    print(f"Ytest : {y_test}")

    chain.fit(X_train, y_train)

    print(f"Ordre utilisé : {chain.order_}")

    # Prédire pour l'exemple de test
    y_pred_single = chain.predict(X_test)

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

print(f"Label-based accuracy : {label_based_accuracy:.4f}")
