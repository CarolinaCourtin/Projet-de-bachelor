# Projet de Bachelor : interpréter des questionnaires UX Attrakdiff avec le machine learning

*Projet de Bachelor, Systèmes d'information et science des services, Université de Genève, printemps 2024 · supervisé par le Pr Patrick Roth*

Le questionnaire **AttrakDiff** sert à évaluer l'expérience utilisateur d'une interface. Il produit des scores chiffrés sur 28 paires de mots (*compliqué/simple*, *laid/beau*…), que le designer doit ensuite traduire lui-même en problèmes concrets à corriger. Ce projet automatise cette étape d'interprétation. Un modèle de machine learning prédit, à partir des résultats AttrakDiff, les **points faibles de l'interface** (clarté, créativité, esthétisme, intuitivité, manque d'informations, professionnalisme). Une application web propose ensuite des **solutions de design** et des **techniques UX** adaptées à chaque problème.

| Accueil | Saisie des résultats | Résultats |
|---|---|---|
| ![Accueil](screenshots/home.png) | ![Formulaire](screenshots/form.png) | ![Résultats](screenshots/results.png) |

## Démarche

1. **Constitution du jeu de données** : des évaluations AttrakDiff tirées d'articles scientifiques et de projets d'étudiants, chacune étiquetée avec les problèmes d'interface identifiés.
2. **Comparaison de 24 configurations** de classification multi-label, évaluées par validation croisée *leave-one-out* :
   - 6 modèles : Naive Bayes, arbre de décision, Random Forest, KNN, régression logistique et SVM ;
   - 2 stratégies multi-label : *One-vs-Rest* et *Classifier Chains* ;
   - 2 niveaux de détail en entrée : les 28 paires de mots, ou les 4 moyennes par dimension.
3. **Modèle retenu** : Random Forest avec Classifier Chains sur les valeurs détaillées. Il obtient une précision par étiquette de 0,76 et une correspondance exacte de 0,36, des scores limités surtout par la petite taille du jeu de données.
4. **Application web Flask** : elle intègre le modèle entraîné et l'associe aux solutions et techniques correspondantes.

## Technologies

Python, scikit-learn, NumPy, Flask, HTML/CSS (Bootstrap)

## Structure

```
├── app/                    # Application web Flask (modèle entraîné, templates, solutions et techniques UX)
├── predictions/            # Code de prédiction utilisé par l'application
├── training/               # Les 24 configurations testées (LOOCV)
│   ├── OVR/                #   One-vs-Rest       → mean_values/ et detailed_values/
│   └── classifier_chains/  #   Classifier Chains → mean_values/ et detailed_values/
├── tests_moins_un/         # Tests en retirant un questionnaire du jeu d'entraînement
└── questionnaires/         # Jeu de données AttrakDiff (JSON) et questionnaires de test
```
