# Pokémon Data Engineering Task

## Task Overview

This repository contains solutions for the Data Engineer (Python, SQL) test task. The goal was to analyze Pokémon data, rank Pokémon by combat effectiveness and type advantage, and visualize results in interactive dashboards. The project includes Easy, Normal, and Hard modes.

### Task Instructions Summary:

* **Task 1:** Collect Pokémon data from provided sources.
* **Task 2:** Rank Pokémon effectiveness (stats and type advantages).
* **Task 3:** Create interactive dashboards to visualize and filter Pokémon rankings.

---

## Project Structure & Workflow

### 1. Data Collection

* **Easy Mode** (`first_task_easy.py`):

  * Fetches Pokémon data from provided CSV (1049 rows).
  * Outputs `pokemon_data.csv` and SQLite database (`pokemon.db`).
  * CSV and database stored in `data/` and `db/` folders respectively.

* **Hard Mode** (`first_task_hard.py`):

  * Parses Pokémon data from [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number).
  * Outputs `parsed_data.csv`.

### 2. Pokémon Ranking

* **Easy Mode** (`second_easy_ranking.py`):

  * Calculates Pokémon strength using provided formula:

    ```
    ([Attack of attacker] - [Defense of defender]) * 0.8 + ([Sp. Attack of attacker] - [Sp. Defense of defender]) * 0.2
    ```
  * Groups results by Pokémon SERIAL to ensure unique Pokémon ranking (reduces dataset from 1049 to 1042 rows).
  * Outputs `ranked_pokemon_easy.csv` and saves data into SQLite.
  * **Additional solution:** (`secondTask_easy_sql.py`): Provided alternative SQL solution demonstrating ranking logic fully in SQL.

* **Normal Mode** (`Second_normal_mode_type.py`):

  * Calculates effectiveness of each Pokémon type against others using provided [type effectiveness matrix](https://img.pokemondb.net/images/typechart.png).
  * Outputs `ranked_pokemon_normal.csv`.

* **Hard Mode** (`second_hard_sql.py`):

  * Combines Easy mode (stat-based ranking) and Normal mode (type-based ranking) into a comprehensive Pokémon ranking dataset (`combined_ranked_pokemon.csv`).
  * This combined dataset is used for Task 3.

### 3. Interactive Dashboards

* **Easy Mode (Streamlit)** (`pokemon_dashboard.py`):

  * Streamlit-based interactive dashboard for exploring Pokémon rankings.
  * Users can filter by Pokémon type and rank.

* **Normal Mode (Google Looker Studio)**:

  * Interactive dashboard using Google Sheets and Looker Studio.
  * Includes filtering by primary and secondary Pokémon types.
  * Displays KPIs (highest effectiveness, highest combat power), ranked tables, and visualizations of Pokémon types.

---

## Files and Directories

``` SCANDIWEB_TASK folder
.
├── data
│   ├── combined_ranked_pokemon.csv
│   ├── parsed_data.csv
│   ├── pokemon_data.csv
│   ├── ranked_pokemon_easy.csv
│   └── ranked_pokemon_normal.csv
│
├── db
│   └── pokemon_scraped.db
│   └── pokemon.db
│
├── first_task_easy.py
├── first_task_hard.py
├── pokemon_dashboard.py
├── Second_easy_ranking.py
├── secondTask_easy_sql.py (Alternative SQL solution provided for demonstration)
├── Second_normal_mode_type.py
├── second_hard_sql.py
└── README.md
```

---

## Logic

### Logic & Approach

* **Data Collection**: Python `requests`, `BeautifulSoup`, and `pandas` for efficient web scraping and CSV handling.
* **Ranking Calculations**: Pandas DataFrames for flexibility, readability, and performance.
* **Database Integration**: SQLite for ease of setup and data manipulation.


---

## AI Assistance

* Used ChatGPT extensively to:

  * Clarify task requirements and breakdown the assignment into clear, manageable steps.
  * Debug Python Code and optimize pandas operations.
  * Guide through unfamiliar tools (Looker Studio setup, Streamlit deployment).
  * Assist in interpreting results and troubleshooting unexpected behaviors, particularly during data cleaning and visualization steps.

---

## Links to Interactive Dashboards

* **Google Spreadsheet:** \[https://docs.google.com/spreadsheets/d/14GUl8RGSYSAAipp1FNHYuyt0MmoCo9Zj8Q6McIWgfbY/edit?usp=sharing)]
* **Looker Studio Dashboard:** \[https://lookerstudio.google.com/reporting/b6b9eb5b-7db2-41f5-af86-7ccd1b169eba]

---

## Submission Instructions

All deliverables are compiled into a single Google document, accessible via the provided link. The document has been shared with required access levels.

* Google Document link (containing GitHub and dashboards links): \[Insert Link Here]

Shared with:

* **[edgars.dumins@scandiweb.com](mailto:edgars.dumins@scandiweb.com)** (Google Spreadsheet and Looker Studio)
* **[tests@scandiweb.com](mailto:tests@scandiweb.com)** (Google Document link with all resources)

---
