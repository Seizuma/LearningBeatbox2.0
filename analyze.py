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

        # Appliquer un groupement par fenêtres temporelles
        data['time'] = pd.to_numeric(data['time'], errors='coerce')
        data = data.sort_values(by='time')

        # Utiliser une fenêtre de 0,1 seconde pour regrouper les sons similaires
        window_size = 0.1
        grouped_data = []
        current_group = []
        current_time = data.iloc[0]['time']

        for _, row in data.iterrows():
            if row['time'] <= current_time + window_size:
                current_group.append(row)
            else:
                if current_group:
                    # Calculer la moyenne pondérée pour l'intensité, la fréquence et la puissance
                    avg_intensity = sum(r['intensity'] for r in current_group) / len(current_group)
                    avg_frequency = sum(r['frequency'] for r in current_group) / len(current_group)
                    avg_power = sum(r['power'] for r in current_group) / len(current_group)
                    winner = current_group[0]['winner']  # Assumer que le son reste le même dans la fenêtre
                    grouped_data.append({
                        'time': current_time,
                        'winner': winner,
                        'intensity': avg_intensity,
                        'frequency': avg_frequency,
                        'power': avg_power,
                        'quality': 'good' if avg_power > 50000 else 'bad'  # Critère simplifié pour l'exemple
                    })
                current_time = row['time']
                current_group = [row]

        # Ajouter le dernier groupe
        if current_group:
            avg_intensity = sum(r['intensity'] for r in current_group) / len(current_group)
            avg_frequency = sum(r['frequency'] for r in current_group) / len(current_group)
            avg_power = sum(r['power'] for r in current_group) / len(current_group)
            winner = current_group[0]['winner']
            grouped_data.append({
                'time': current_time,
                'winner': winner,
                'intensity': avg_intensity,
                'frequency': avg_frequency,
                'power': avg_power,
                'quality': 'good' if avg_power > 50000 else 'bad'
            })

        # Convertir en DataFrame
        grouped_df = pd.DataFrame(grouped_data)

        # Calculer les statistiques
        stats = grouped_df.groupby('winner').agg(
            count=('winner', 'size'),
            avg_intensity=('intensity', 'mean'),
            avg_frequency=('frequency', 'mean'),
            avg_power=('power', 'mean'),
            good_quality_count=('quality', lambda x: (x == 'good').sum()),
            bad_quality_count=('quality', lambda x: (x == 'bad').sum()),
            neutral_quality_count=('quality', lambda x: (x == 'neutral').sum() if 'neutral' in x else 0)
        ).reset_index()

        stats['avg_intensity'] = stats['avg_intensity'].apply(lambda x: f"{x:.2f} %")
        stats['avg_frequency'] = stats['avg_frequency'].apply(lambda x: f"{x:.2f} Hz")
        stats['avg_power'] = stats['avg_power'].apply(lambda x: f"{x:.2f} W")

        print(f"Stats calculated:\n{stats}")

        return stats.to_dict(orient='records')

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}
