import json
import os.path
import os

def add_data(questionnaire_name):

    choice = None

    file_path = 'all_questionnaires.json'

    with open(file_path, 'r') as fichier:

        data = json.load(fichier)

        while choice != 7:

            choice = int(input(
                "Which categroy to add data to :\n | 1 - valeurs_moyennes\n | 2 - paire_de_mots\n | 3 - portfolio\n | 4 - valeurs_generales\n | 5 - problemes et solutions\n | 6 - leave\n Your choice : "))

            if choice == 1:

                print("Enter values for valeurs_moyennes (press Enter to skip):")
                QP = input("Value for QP : ")
                if QP:
                    data[questionnaire_name]["valeurs_moyennes"]["QP"] = float(QP)

                QHS = input("Value for QHS : ")
                if QHS:
                    data[questionnaire_name]["valeurs_moyennes"]["QHS"] = float(QHS)

                QHI = input("Value for QHI : ")
                if QHI:
                    data[questionnaire_name]["valeurs_moyennes"]["QHI"] = float(QHI)

                ATT = input("Value for ATT : ")
                if ATT:
                    data[questionnaire_name]["valeurs_moyennes"]["ATT"] = float(ATT)

            elif choice == 2:
                print("Enter values for paire_de_mots (press Enter to skip):")
                for i in data[questionnaire_name]["paire_de_mots"]:
                    print(f"{i} values:")
                    for j in data[questionnaire_name]["paire_de_mots"][i]:
                        new_value = input(f"Value for {j}: ")
                        if new_value:
                            data[questionnaire_name]["paire_de_mots"][i][j] = float(new_value)

            elif choice == 3:
                print("Enter values for portfolio (press Enter to skip):")
                data[questionnaire_name]["portfolio"]["moyenne hedonique"] = float(input("Moyenne hedonique: "))
                data[questionnaire_name]["portfolio"]["moyenne pragmatique"] = float(input("Moyenne pragmatique: "))
                data[questionnaire_name]["portfolio"]["statut"] = input("Statut: ")
                intervalle_confiance = input("Intervalle confiance: ")
                if intervalle_confiance:
                    data[questionnaire_name]["portfolio"]["intervalle_confiance"] = float(intervalle_confiance)

            elif choice == 4:
                print("Enter values for valeurs_generales (press Enter to skip):")
                marge_erreur = input("Marge d'erreur: ")
                if marge_erreur:
                    data[questionnaire_name]["valeurs_generales"]["marge_erreur"] = float(marge_erreur)
                echantillon = input("Echantillon: ")
                if echantillon:
                    data[questionnaire_name]["valeurs_generales"]["echantillon"] = float(echantillon)

            elif choice == 5:
                print("Enter problems comments (press Enter to skip):")
                # comment_count = 1
                while True:
                    domaine_probleme = str(input("Probleme : "))
                    conclusion = str(input("Conclusion : "))
                    # comment_key = f"probleme {comment_count}"
                    # comment_text = input(f"Probleme {comment_count}: ")
                    if domaine_probleme:
                        data[questionnaire_name]["probleme"][domaine_probleme] = conclusion
                    else:
                        break
                    # comment_count += 1

            elif choice == 6:

                break

    with open(file_path, 'w') as fichier:

        json.dump(data, fichier, indent=4)



# ¨¨¨¨¨¨VOIR COMMENT FAIRE UNE BOUCLE PLUTOT
def add_questionnaire(questionnaire_name):

    file_path = 'all_questionnaires.json'

    categories = {

        "valeurs_moyennes": {

            "QP":None,
            "QHS":None,
            "QHI":None,
            "ATT":None
        },
        "paire_de_mots": {

            "QP": {

                "technique/humain": None,
                "complique/simple": None,
                "pas pratique/pratique": None,
                "fastidieux/efficace":None,
                "imprevisible/previsible": None,
                "confus/clair": None,
                "incontrolable/maitrisable":None
            },
            "QHS": {
                "conventionnel/original":None,
                "sans imagination/creatif":None,
                "prudent/audacieux":None,
                "conservateur/novateur": None,
                "ennuyeux/captivant": None,
                "peu exigeant/challenging": None,
                "commun/nouveau": None
            },
            "QHI": {
                "m'isole/me sociabilise":None,
                "amateur/professionel": None,
                "de mauvais gout/de bon gout": None,
                "bas de gamme/haut de gamme": None,
                "m'exclut/m'integre": None,
                "me depare des autres/me rapproche des autre": None,
                "non presentable/presentable": None
            },
            "ATT": {
                "deplaisant/plaisant": None,
                "laid/beau": None,
                "desagreable/agreable": None,
                "rebutant/attirant": None,
                "mauvais/bon": None,
                "repoussant/attrayant": None,
                "decourageant/motivant": None
            }
        },

        "portfolio": {

            "moyenne hedonique": None,
            "moyenne pragmatique": None,
            "statut":None,
            "intervalle confiance":None
        },

        "valeurs_generales": {

            "marge d'erreur":None,
            "echantillon":None

        },

        "probleme":{

        },
    }

    if os.path.isfile(file_path):  # Vérifier si le fichier existe

        with open(file_path, 'r+') as fichier:

            data = json.load(fichier)

            data[questionnaire_name] = categories

            fichier.seek(0)  # Retourner au début du fichier

            json.dump(data, fichier, indent=4)

    else:
        with open(file_path, 'w') as fichier: # création d'un nouveau fichier
            data = {questionnaire_name: categories}
            fichier.seek(0)
            json.dump(data, fichier, indent=4)


questionnaire_name = str(input("Questionnaire name : "))

add_questionnaire(questionnaire_name)
add_data(questionnaire_name)