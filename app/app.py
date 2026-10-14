import sys
import os

# Ajouter le dossier parent 'projetbachelor' au chemin de recherche de modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, url_for, redirect, session
from predictions import predictions_with_techniques

# jmdcwpopokdèpk


app = Flask(__name__)

app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=["GET", "POST"])
def files():
    if request.method == "POST":
        # Récupérer les valeurs des champs de formulaire
        form_data = {
            #"questionnaire_name": request.form.get("questionnaire_name"),
            "value_technique_humain": request.form.get("value_technique_humain"),
            "value_complique_simple": request.form.get("value_complique_simple"),
            "value_pas_pratique_pratique": request.form.get("value_pas_pratique_pratique"),
            "value_fastidieux_efficace": request.form.get("value_fastidieux_efficace"),
            "value_imprevisible_previsible": request.form.get("value_imprevisible_previsible"),
            "value_confus_clair": request.form.get("value_confus_clair"),
            "value_incontrolable_maitrisable": request.form.get("value_incontrolable_maitrisable"),
            "value_conventionnel_original": request.form.get("value_conventionnel_original"),
            "value_sans_imagination_creatif": request.form.get("value_sans_imagination_creatif"),
            "value_prudent_audacieux": request.form.get("value_prudent_audacieux"),
            "value_conservateur_novateur": request.form.get("value_conservateur_novateur"),
            "value_ennuyeux_captivant": request.form.get("value_ennuyeux_captivant"),
            "value_peu_exigeant_challenging": request.form.get("value_peu_exigeant_challenging"),
            "value_commun_nouveau": request.form.get("value_commun_nouveau"),
            "value_m_isole_me_sociabilise": request.form.get("value_m_isole_me_sociabilise"),
            "value_amateur_professionnel": request.form.get("value_amateur_professionnel"),
            "value_de_mauvais_gout_de_bon_gout": request.form.get("value_de_mauvais_gout_de_bon_gout"),
            "value_bas_de_gamme_haut_de_gamme": request.form.get("value_bas_de_gamme_haut_de_gamme"),
            "value_m_exclut_m_integre": request.form.get("value_m_exclut_m_integre"),
            "value_me_separe_des_autres_me_rapproche_des_autres": request.form.get("value_me_separe_des_autres_me_rapproche_des_autres"),
            "value_non_presentable_presentable": request.form.get("value_non_presentable_presentable"),
            "value_deplaisant_plaisant": request.form.get("value_deplaisant_plaisant"),
            "value_laid_beau": request.form.get("value_laid_beau"),
            "value_desagreable_agreable": request.form.get("value_desagreable_agreable"),
            "value_rebutant_attirant": request.form.get("value_rebutant_attirant"),
            "value_mauvais_bon": request.form.get("value_mauvais_bon"),
            "value_repoussant_attrayant": request.form.get("value_repoussant_attrayant"),
            "value_decourageant_motivant": request.form.get("value_decourageant_motivant")
        }

        '''for key, value in form_data.items():
            print(f"{key}: {value}")'''

        questionnaire_name = request.form.get("questionnaire_name")
        problemes, solutions, techniques = predictions_with_techniques.prediction(questionnaire_name, form_data)

        # Stocker les listes dans la session
        session['problemes'] = problemes
        session['solutions'] = solutions
        session['techniques'] = techniques

        return redirect(url_for('results'))
        # return redirect(url_for('results'))

    return render_template('files.html')

@app.route('/results', methods=["GET", "POST"])
def results():
    problemes = session.get('problemes', [])
    solutions = session.get('solutions', [])
    techniques = session.get('techniques', [])

    return render_template('results.html', problemes=problemes, solutions=solutions, techniques=techniques)

if __name__ == '__main__':

    app.run()