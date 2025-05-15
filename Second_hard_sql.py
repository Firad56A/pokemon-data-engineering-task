import sqlite3
import pandas as pd

# Connect to the database
DB_FILE_PATH = 'db/pokemon.db'
conn = sqlite3.connect(DB_FILE_PATH)

# Execute the SQL query to combine the results
query = '''
    CREATE TABLE IF NOT EXISTS Pokemon_Ranking AS
    SELECT 
        rp.Serial,
        rp.NAME,
        rpn.TYPE1,
        rpn.TYPE2,
        rpn.Effectiveness_Type1,
        rpn.Effectiveness_Type2,
        (rpn.Effectiveness_Type1 + rpn.Effectiveness_Type2) AS Overall_Effectiveness,
        rp.Total_Effectiveness AS Combat_Power
    FROM Ranked_Pokemon AS rp
    JOIN Ranked_Pokemon_Normal AS rpn
    ON rp.Serial = rpn.Serial
    ORDER BY Combat_Power DESC, Overall_Effectiveness DESC;
'''

# Execute the query
conn.execute(query)
conn.commit()

# Load the combined data into a DataFrame
df_combined = pd.read_sql('SELECT * FROM Pokemon_Ranking', conn)

# Save the result to CSV
RANKED_CSV_PATH = 'data/combined_ranked_pokemon.csv'
df_combined.to_csv(RANKED_CSV_PATH, index=False)
print(f'Ranked data saved to {RANKED_CSV_PATH}')

# Close the connection
conn.close()
