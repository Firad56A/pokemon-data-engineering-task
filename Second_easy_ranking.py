import os
import sqlite3
import pandas as pd

# Directory Setup
DB_DIR = 'db'
DB_FILE_PATH = os.path.join(DB_DIR, 'pokemon.db')
RANKED_CSV_PATH = os.path.join('data', 'ranked_pokemon_easy.csv')

# Connect to the database
conn = sqlite3.connect(DB_FILE_PATH)

# Extract Data
query = '''
    SELECT Serial, NAME, ATK, DEF, SP_ATK, SP_DEF
    FROM Pokemon
    GROUP BY Serial
'''

df = pd.read_sql(query, conn)

# Initialize an empty list to store results
results = []

# Iterate over each Pokémon as the attacker
for index, attacker in df.iterrows():
    total_score = 0
    # Iterate over each Pokémon as the defender
    for _, defender in df.iterrows():
        # Skip self-comparison
        if attacker['NAME'] != defender['NAME']:
            # Calculate the score for each pair
            physical_score = (attacker['ATK'] - defender['DEF']) * 0.8
            special_score = (attacker['SP_ATK'] - defender['SP_DEF']) * 0.2
            # Accumulate the total score
            total_score += physical_score + special_score

    # Append the results with the serial number included
    results.append((attacker['SERIAL'],attacker['NAME'], total_score))

# Create a DataFrame for the results, including the serial number
ranked_df = pd.DataFrame(results, columns=['SERIAL','NAME', 'Total_Effectiveness'])

# Sort by Total_Effectiveness
ranked_df = ranked_df.sort_values(by='Total_Effectiveness', ascending=False)

# Save to CSV
ranked_df.to_csv(RANKED_CSV_PATH, index=False)
print(f'Ranked data saved to {RANKED_CSV_PATH}')

# Save to Database with Serial included
ranked_df.to_sql('Ranked_Pokemon', conn, if_exists='replace', index=False)
print('Ranked data successfully inserted into the database.')

# Close the connection
conn.close()
print('Database connection closed.')
