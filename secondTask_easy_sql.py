import os
import sqlite3
import pandas as pd

# Directory Setup
DB_DIR = 'db'
DB_FILE_PATH = os.path.join(DB_DIR, 'pokemon.db')
RANKED_CSV_PATH = os.path.join('data', 'ranked_pokemon_easy_sql_output.csv')

# Connect to the database
conn = sqlite3.connect(DB_FILE_PATH)

# SQL Query with Self Join and including SERIAL
query = '''
    SELECT 
        attacker.SERIAL AS ID,
        attacker.NAME AS Attacker,
        attacker.SERIAL,  -- Ensure SERIAL is included
        SUM(
            (attacker.ATK - defender.DEF) * 0.8 + 
            (attacker.SP_ATK - defender.SP_DEF) * 0.2
        ) AS Total_Effectiveness
    FROM Pokemon AS attacker
    LEFT JOIN Pokemon AS defender 
    ON attacker.SERIAL != defender.SERIAL
    GROUP BY attacker.SERIAL
    ORDER BY Total_Effectiveness DESC;
'''

# Execute the query and load the data into DataFrame
df = pd.read_sql(query, conn)

# Save to CSV
df.to_csv(RANKED_CSV_PATH, index=False)
print(f'Ranked data saved to {RANKED_CSV_PATH}')

# Insert the ranked data into a table in the database, including SERIAL
df.to_sql('Ranked_Pokemon_Easy_SQL', conn, if_exists='replace', index=False)
print('Ranked data successfully inserted into the database.')

# Close the connection
conn.close()
print('Database connection closed.')
