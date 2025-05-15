import os
import requests
import pandas as pd
import sqlite3

# Directory Setup
DATA_DIR = 'data'
DB_DIR = 'db'
CSV_FILE_PATH = os.path.join(DATA_DIR, 'pokemon_data.csv')
DB_FILE_PATH = os.path.join(DB_DIR, 'pokemon.db')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# URL of the CSV data
CSV_URL = 'https://gist.githubusercontent.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19/raw/pokemon.csv'

# Download CSV data
print('Downloading Pokemon data...')
response = requests.get(CSV_URL)
with open(CSV_FILE_PATH, 'wb') as file:
    file.write(response.content)
print('Data downloaded and saved as pokemon_data.csv')

# Load CSV data into a DataFrame with error handling
# Noticed an inconsistency in line 1043 with 29 columns instead of 22.
# Using on_bad_lines='skip' to skip problematic lines and proceed with data processing.
print('Loading data into DataFrame...')
df = pd.read_csv(CSV_FILE_PATH, on_bad_lines='skip')
print('Data loaded successfully.')

# Replace None values with empty string '' for columns in the DataFrame
df = df.fillna('')

# Connect to SQLite Database
print('Creating SQLite database...')
conn = sqlite3.connect(DB_FILE_PATH)
cursor = conn.cursor()

# Drop Table if Exists (for testing purposes)
cursor.execute("DROP TABLE IF EXISTS Pokemon")

# Dynamically Create Table based on DataFrame Columns
columns = df.columns.tolist()
column_types = ['INTEGER PRIMARY KEY' if col == 'ID' else 'TEXT' for col in columns]
column_definitions = ', '.join([f'{col} {col_type}' for col, col_type in zip(columns, column_types)])

create_table_query = f"CREATE TABLE IF NOT EXISTS Pokemon ({column_definitions});"
cursor.execute(create_table_query)

# Insert Data
print('Inserting data into the database...')
df.to_sql('Pokemon', conn, if_exists='replace', index=False)
print('Data successfully inserted into the database.')

# Close Connection
conn.close()
print('Database connection closed.')
