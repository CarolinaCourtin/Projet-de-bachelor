from datetime import datetime
import json
import numpy as np
import joblib
import os

def prediction(questionnaire_name, form_data):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    questionnaire_nameee = f'{questionnaire_name}_{timestamp}'
    file_name = f'{questionnaire_name}_{timestamp}.json'
    file_path = os.path.join("../questionnaires/prediction_questionnaires_app", file_name)

    data_user_input = {
        "paire_de_mots": {
            "QP": {
                "technique/humain": float(form_data.get("value_technique_humain", 0)),
                "complique/simple": float(form_data.get("value_complique_simple", 0)),
                "pas pratique/pratique": float(form_data.get("value_pas_pratique_pratique", 0)),
                "fastidieux/efficace": float(form_data.get("value_fastidieux_efficace", 0)),
                "imprevisible/previsible": float(form_data.get("value_imprevisible_previsible", 0)),
                "confus/clair": float(form_data.get("value_confus_clair", 0)),
                "incontrolable/maitrisable": float(form_data.get("value_incontrolable_maitrisable", 0))
            },
            "QHS": {
                "conventionnel/original": float(form_data.get("value_conventionnel_original", 0)),
                "sans imagination/creatif": float(form_data.get("value_sans_imagination_creatif", 0)),
                "prudent/audacieux": float(form_data.get("value_prudent_audacieux", 0)),
                "conservateur/novateur": float(form_data.get("value_conservateur_novateur", 0)),
                "ennuyeux/captivant": float(form_data.get("value_ennuyeux_captivant", 0)),
                "peu exigeant/challenging": float(form_data.get("value_peu_exigeant_challenging", 0)),
                "commun/nouveau": float(form_data.get("value_commun_nouveau", 0))
            },
            "QHI": {
                "m'isole/me sociabilise": float(form_data.get("value_m_isole_me_sociabilise", 0)),
                "amateur/professionel": float(form_data.get("value_amateur_professionnel", 0)),
                "de mauvais gout/de bon gout": float(form_data.get("value_de_mauvais_gout_de_bon_gout", 0)),
                "bas de gamme/haut de gamme": float(form_data.get("value_bas_de_gamme_haut_de_gamme", 0)),
                "m'exclut/m'integre": float(form_data.get("value_m_exclut_m_integre", 0)),
                "me depare des autres/me rapproche des autre": float(
                    form_data.get("value_me_separe_des_autres_me_rapproche_des_autres", 0)),
                "non presentable/presentable": float(form_data.get("value_non_presentable_presentable", 0))
            },
            "ATT": {
                "deplaisant/plaisant": float(form_data.get("value_deplaisant_plaisant", 0)),
                "laid/beau": float(form_data.get("value_laid_beau", 0)),
                "desagreable/agreable": float(form_data.get("value_desagreable_agreable", 0)),
                "rebutant/attirant": float(form_data.get("value_rebutant_attirant", 0)),
                "mauvais/bon": float(form_data.get("value_mauvais_bon", 0)),
                "repoussant/attrayant": float(form_data.get("value_repoussant_attrayant", 0)),
                "decourageant/motivant": float(form_data.get("value_decourageant_motivant", 0))
            }
        }
    }

    X_new = []

    problemes = []
    techniques = []
    solutions = []

    for categorie, paires in data_user_input["paire_de_mots"].items():

        # print(f'categorie : {categorie}')
        # print(f'paires de mots : {paires}')
        for paire, valeur in paires.items():
            print(f"{paire}: {valeur}")
            X_new.append(float(valeur))

    print(f"Valeur de data : {X_new}")

    modele_charge = joblib.load('random_forest_chains_model.pkl')

    X_flattened = np.array(X_new)

    X_new_reshaped = X_flattened.reshape(1, -1)

    categories = ['Clarte', 'Creativite', 'Esthetisme', 'Intuitivite', 'Manque d informations', 'Professionnalisme']

    predictions = modele_charge.predict(X_new_reshaped)

    predicted_indices = np.where(predictions[0] == 1)[0]

    predicted_categories = [categories[i] for i in predicted_indices]


    with open('techniques.json', 'r') as f:

        data = json.load(f)

        for probleme in predicted_categories:

            problemes.append(probleme)

            techniques.append(data[probleme])

    with open('problems_with_solutions.json', 'r') as f:

        data = json.load(f)

        for probleme in predicted_categories:

            solutions.append(data[probleme])



    with open(file_path, 'w') as fichier:

        data2 = {questionnaire_nameee: data_user_input}

        json.dump(data2, fichier, indent=4)

    return problemes, solutions, techniques




