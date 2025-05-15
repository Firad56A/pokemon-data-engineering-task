import sqlite3
import pandas as pd

# Type Effectiveness Chart (Complete)
type_chart = {
    'Normal': {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
    'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2},
    'Water': {'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2, 'Rock': 2, 'Dragon': 0.5},
    'Electric': {'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0, 'Flying': 2, 'Dragon': 0.5},
    'Grass': {'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2, 'Dragon': 0.5, 'Steel': 0.5},
    'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 0.5, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Steel': 0.5},
    'Fighting': {'Normal': 2, 'Ice': 2, 'Rock': 2, 'Dark': 2, 'Steel': 2, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Fairy': 0.5, 'Ghost': 0},
    'Poison': {'Grass': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Fairy': 2},
    'Ground': {'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Poison': 2, 'Flying': 0, 'Bug': 0.5, 'Rock': 2, 'Steel': 2},
    'Flying': {'Grass': 2, 'Electric': 0.5, 'Fighting': 2, 'Bug': 2, 'Rock': 0.5, 'Steel': 0.5},
    'Psychic': {'Fighting': 2, 'Poison': 2, 'Psychic': 0.5, 'Dark': 0, 'Steel': 0.5},
    'Bug': {'Fire': 0.5, 'Grass': 2, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2, 'Ghost': 0.5, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5},
    'Rock': {'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2, 'Bug': 2, 'Steel': 0.5},
    'Ghost': {'Normal': 0, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5},
    'Dragon': {'Dragon': 2, 'Steel': 0.5, 'Fairy': 0},
    'Dark': {'Fighting': 0.5, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Fairy': 0.5},
    'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2, 'Rock': 2, 'Steel': 0.5, 'Fairy': 2},
    'Fairy': {'Fire': 0.5, 'Fighting': 2, 'Poison': 0.5, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5}
}

# Connect to the database
DB_FILE_PATH = 'db/pokemon.db'
conn = sqlite3.connect(DB_FILE_PATH)

# Query to extract Name, Type1 and Type2 from the Pokemon table
query = '''
    SELECT SERIAL, NAME, TYPE1, TYPE2
    FROM Pokemon
'''
df = pd.read_sql(query, conn)

# Calculate Effectiveness Score
def calculate_effectiveness(pokemon_type):
    score = 0
    for target_type in type_chart.keys():
        if pokemon_type in type_chart:
            effectiveness = type_chart[pokemon_type].get(target_type, 1)
            score += effectiveness
    return score

df['TYPE2'] = df['TYPE2'].fillna('')

# Apply Effectiveness Calculation for Type1 and Type2
df['Effectiveness_Type1'] = df['TYPE1'].apply(calculate_effectiveness)
df['Effectiveness_Type2'] = df['TYPE2'].apply(lambda x: calculate_effectiveness(x) if x != '' else 0)

# Calculate Total Effectiveness
df['Total_Effectiveness'] = df['Effectiveness_Type1'] + df['Effectiveness_Type2']
# Sort Pokémon by Total Effectiveness (Highest to Lowest)
df = df.sort_values(by='Total_Effectiveness', ascending=False)

# Save to CSV
RANKED_CSV_PATH = 'data/ranked_pokemon_normal.csv'
df.to_csv(RANKED_CSV_PATH, index=False)
print(f'Ranked data saved to {RANKED_CSV_PATH}')

# Save to Database
df.to_sql('Ranked_Pokemon_Normal', conn, if_exists='replace', index=False)
print('Ranked data successfully inserted into the database.')

# Close the connection
conn.close()
print('Database connection closed.')
