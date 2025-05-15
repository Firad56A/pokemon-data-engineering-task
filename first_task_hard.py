import os
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Directory Setup
DATA_DIR = 'data'
DB_DIR = 'db'
SCRAPED_CSV_PATH = os.path.join(DATA_DIR, 'parsed_data.csv')
DB_FILE_PATH = os.path.join(DB_DIR, 'pokemon_scraped.db')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# URL of the webpage to scrape
SCRAPE_URL = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'

print('Starting data scraping...')
response = requests.get(SCRAPE_URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Locate all generation tables
tables = soup.find_all('table', {'class': 'roundy'})
data = []

for table in tables:
    rows = table.find_all('tr')
    # Extract headers dynamically
    header = [th.text.strip() for th in rows[0].find_all('th')]

    # Ensure that we have the expected columns, including MS
    if 'Ndex' in header and 'Pokémon' in header and 'Type' in header and 'MS' in header:
        for row in rows[1:]:
            cols = row.find_all('td')
            # Ensure we have the correct number of columns
            if len(cols) >= 4:
                ndex = cols[0].text.strip().replace('#', '')  # Remove '#' for ID (Ndex)
                name = cols[2].text.strip()  # Extract Pokémon Name
                ms = cols[1].text.strip()
                 
                # Handle Types
                types = [col.text.strip() for col in cols[3:]]
                # Ensure we only extract up to 2 types
                types = types[:2] + [''] * (2 - len(types))  # Fill missing types with empty strings
                # Adjust to dynamically handle Type1 and Type2
                                # Handle cases where nDex is missing (i.e., fill it with the previous value)
                while len(types) < 2:
                    types.append('NULL')  # Fill missing types with 'NULL' (or 'N/A')

                if not ndex:
                    ndex = last_ndex
                    name = ms
                    ms = ''
                    types = [col.text.strip() for col in cols[2:]]
                else:
                    last_ndex = ndex
                #      # Handle the case where `name` is actually a concatenation of base name and form name
                # # Handle the case where `name` is actually a concatenation of base name and form name
                # # Example: "OgerponWellspring Mask" → "Ogerpon Wellspring Mask"
                # # Check for uppercase letter followed by a lowercase letter to identify base name and form name
                # if name:
                #     # Split by first capital letter after the base name
                #     parts = []
                #     temp = ""
                #     for char in name:
                #         # If we find a capital letter after some content in `temp`, start a new part
                #         if char.isupper() and temp:
                #             parts.append(temp)
                #             temp = char
                #         else:
                #             temp += char
                #     parts.append(temp)  # Add the last part
                    
                #     # Combine parts with a space
                #     name = " ".join(parts)


                type1 = types[0] if len(types) > 0 else 'NULL'
                type2 = types[1] if len(types) > 1 else 'NULL'



                # Add the row with the correct 'Code' (nDex), 'MS' and types
                data.append([ndex, ms, name, type1, type2])


# Create DataFrame with 'Code' as the column for the ID and 'MS' for image
columns = ['Code', 'MS', 'Name', 'Type1', 'Type2']
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv(SCRAPED_CSV_PATH, index=False)
print(f'Data saved to {SCRAPED_CSV_PATH}')

#  --- Insert into Database ---

# Connect to SQLite database
conn = sqlite3.connect(DB_FILE_PATH)
cursor = conn.cursor()

# Create table with custom primary key (ID)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pokemon_Scraped (
    Unique_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code INTEGER,
    MS TEXT,
    Name TEXT,
    Type1 TEXT,
    Type2 TEXT
);
''')

# Insert data into the database
for row in data:
    cursor.execute('''
    INSERT INTO Pokemon_Scraped (Code, MS, Name, Type1, Type2)
    VALUES ( ?, ?, ?, ?, ?)
    ''', row)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f'Data with custom primary key saved to database: {DB_FILE_PATH}')