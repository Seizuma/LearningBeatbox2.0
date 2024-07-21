import pandas as pd
import csv

def analyze_replay(replay_file):
    try:
        # Lire le fichier CSV manuellement et ignorer la colonne "actions"
        rows = []
        headers = []
        with open(replay_file, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)  # Lire les en-têtes
            headers = [header for header in headers if header and header != 'actions']  # Enlever 'actions' et les en-têtes vides
            for row in csvreader:
                if row:  # Ignorer les lignes vides
                    rows.append([value for i, value in enumerate(row) if i < len(headers)])  # S'assurer de ne pas dépasser les en-têtes

        # Convertir les données en DataFrame
        data = pd.DataFrame(rows, columns=headers)
        print("Data loaded successfully")
        print(data.head())  # Afficher les premières lignes du DataFrame chargé

        # Correction des noms de colonnes mal interprétés
        data.columns = [col.strip() for col in data.columns]

        # Supprimer les lignes où toutes les valeurs sont NaN
        data.dropna(how='all', inplace=True)

        # Supprimer les lignes de "silence"
        data = data[data['winner'].notna() & (data['winner'].str.lower() != 'silence')]
        print(f"Filtered data:\n{data.head()}")

        if data.empty:
            print("No valid data to analyze after filtering out 'silence'")
            return {'error': 'No valid data to analyze after filtering out silence'}

        # Convertir les colonnes numériques en types appropriés
        numeric_columns = data.columns.drop('winner')
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Filtrer les sons détectés en dessous de 80% d'intensité
        data = data[data['intensity'] >= 80]

        # Filtrer les sons détectés en dessous de 100 d'intensité pour éliminer les faux positifs
        data = data[data['intensity'] >= 100]

        # Filtrer les sons détectés en dessous de certains seuils de fréquence et de puissance
        data = data[(data['frequency'] >= 100) & (data['power'] >= 1000)]
        print(f"Filtered data with intensity, frequency, and power thresholds:\n{data.head()}")

        # Filtrer les sons détectés en dessous de 0.300s
        def filter_close_sounds(data, time_threshold=0.300):
            filtered_data = []
            previous_time = -time_threshold
            previous_winner = None

            for index, row in data.iterrows():
                current_time = row['time']
                current_winner = row['winner']
                if current_winner != previous_winner or current_time - previous_time >= time_threshold:
                    filtered_data.append(row)
                    previous_time = current_time
                    previous_winner = current_winner

            return pd.DataFrame(filtered_data)

        data['time'] = data['time'].astype(float)
        data = filter_close_sounds(data)
        print(f"Filtered data with time threshold:\n{data.head()}")

        # Déterminer la qualité des sons détectés
        def determine_quality(row):
            winner = row['winner']
            if winner in row.index and pd.notna(row[winner]):
                if row[winner] >= 90:
                    return 'good'
                elif row[winner] < 80:
                    return 'bad'
                else:
                    return 'neutral'
            return 'neutral'

        data['quality'] = data.apply(determine_quality, axis=1)
        print(f"Data with quality:\n{data[['winner', 'quality']].head()}")

        # Calculer les statistiques
        stats = data.groupby('winner').agg(
            count=('winner', 'size'),
            avg_intensity=('intensity', 'mean'),
            avg_frequency=('frequency', 'mean'),
            avg_power=('power', 'mean'),
            good_quality_count=('quality', lambda x: (x == 'good').sum()),
            bad_quality_count=('quality', lambda x: (x == 'bad').sum()),
            neutral_quality_count=('quality', lambda x: (x == 'neutral').sum())
        ).reset_index()
        print(f"Stats calculated:\n{stats}")

        # Calculer la précision globale
        total_sounds = len(data)
        detected_sounds = len(data)
        overall_accuracy = detected_sounds / total_sounds * 100

        results = {
            'stats': stats.to_dict(orient='records'),
            'overall_accuracy': overall_accuracy
        }

        return results
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {'error': f"An unexpected error occurred: {e}"}

# Exemple d'appel de la fonction (à ajuster selon votre contexte)
# result = analyze_replay('path_to_your_csv_file.csv')
# print(result)
