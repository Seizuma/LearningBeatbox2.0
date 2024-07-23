import pandas as pd
import os
import csv

def get_last_replay_file():
    replays_folder = 'data/replays'  # Assuming REPLAYS_FOLDER is 'replays'
    replay_files = [os.path.join(replays_folder, f) for f in os.listdir(replays_folder) if f.endswith('.csv')]
    if replay_files:
        return max(replay_files, key=os.path.getctime)
    else:
        return None

def clean_csv_data(file_path):
    cleaned_rows = []
    headers = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        headers = [header for header in headers if header]  # Enlever les en-têtes vides
        for row in csvreader:
            if len(row) > len(headers):
                row = row[:len(headers)]  # Enlever les colonnes supplémentaires
            if len(row) == len(headers):
                cleaned_rows.append(row)
    return headers, cleaned_rows

def analyze_replay(replay_file, sound_name):
    try:
        headers, cleaned_rows = clean_csv_data(replay_file)

        # Convertir les données en DataFrame
        data = pd.DataFrame(cleaned_rows, columns=headers)
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

        # Filtrer les sons par nom spécifique
        data = data[data['winner'].str.lower() == sound_name.lower()]

        if data.empty:
            print(f"No valid data to analyze for the sound '{sound_name}'")
            return {'error': f"No valid data to analyze for the sound '{sound_name}'"}

        # Filtrer les données avec une puissance >= 100000
        data = data[data['power'] >= 100000]

        if data.empty:
            print(f"No valid data with sufficient power to analyze for the sound '{sound_name}'")
            return {'error': f"No valid data with sufficient power to analyze for the sound '{sound_name}'"}

        # Calculer la moyenne du pourcentage de sûreté, de la puissance et de la fréquence
        avg_surety = data[sound_name].mean()
        avg_power = data['power'].mean()
        avg_frequency = data['frequency'].mean()

        print(f"Average surety for '{sound_name}': {avg_surety:.2f} %")
        print(f"Average power for '{sound_name}': {avg_power:.2f} W")
        print(f"Average frequency for '{sound_name}': {avg_frequency:.2f} Hz")

        return {
            'sound': sound_name,
            'avg_surety': f"{avg_surety:.2f} %",
            'avg_power': f"{avg_power:.2f} W",
            'avg_frequency': f"{avg_frequency:.2f} Hz"
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}

if __name__ == '__main__':
    replay_file = get_last_replay_file()
    if replay_file:
        sound_name = input("Enter the sound name to analyze: ")
        results = analyze_replay(replay_file, sound_name)
        print(results)
    else:
        print("No replay file found")
