import joblib
import numpy as np

directory_path = '../../../models/classifier_chains_DETAILED_VALUES'

loaded_chains = [joblib.load(f'{directory_path}model_chain_{i}.joblib') for i in range(8)]

# Nouvelles données (par exemple, new_X)
new_X = [...]  # Remplacez par vos nouvelles données


np.set_printoptions(precision=4, suppress=True)

X_flattened = []
for sample in X:
    flattened_sample = []
    # Flattening des catégories
    for category in sample[0]:
        flattened_sample.extend(category)
    # Ajout des mesures agrégées
    flattened_sample.extend(sample[1])
    X_flattened.append(flattened_sample)

X_flattened = np.array(X_flattened)

print(X_flattened)

# remplacer par les bonnes données...

# Faire des prédictions avec les chaînes chargées
new_predictions = [chain.predict(new_X) for chain in loaded_chains]

# Calculer la moyenne des prédictions si vous utilisez un ensemble
ensemble_predictions = np.mean(new_predictions, axis=0)

# Binariser les prédictions selon le seuil 0.5
final_predictions = ensemble_predictions >= 0.5

print(final_predictions)