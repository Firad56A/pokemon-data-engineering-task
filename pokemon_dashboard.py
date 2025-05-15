import streamlit as st
import pandas as pd
import altair as alt

# Load the combined Pokémon ranking data (adjust the file path if needed)
df = pd.read_csv('data/combined_ranked_pokemon.csv')

# Clean TYPE2: replace NaN with 'None'
df['TYPE2'] = df['TYPE2'].fillna('None')

# KPIs
st.title("Pokémon Ranking Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Highest Combat Power", f"{df['Combat_Power'].max():,.1f}")
col2.metric("Highest Type Overall Effectiveness", f"{df['Overall_Effectiveness'].max():.1f}")
col3.metric("Most Common Primary Type", df['TYPE1'].mode()[0])

st.write("---")
# Filters
type1_opts = ['All'] + sorted(df['TYPE1'].unique())
type2_opts = ['All'] + sorted(df['TYPE2'].unique())
sel1 = st.selectbox("Primary Type", type1_opts)
sel2 = st.selectbox("Secondary Type", type2_opts)
top_n = st.slider("Show top N Pokémon by Effectiveness", 5, min(200, len(df)), 10)

# Apply filters
filtered = df.copy()
if sel1 != 'All':
    filtered = filtered[filtered['TYPE1'] == sel1]
if sel2 != 'All':
    filtered = filtered[filtered['TYPE2'] == sel2]

# Sort and limit
filtered = filtered.sort_values('Overall_Effectiveness', ascending=False)
top = filtered.head(top_n)

# Display top table
st.subheader(f"Top {top_n} Pokémon")
st.dataframe(top[['NAME', 'TYPE1', 'TYPE2', 'Overall_Effectiveness', 'Combat_Power']])

# Type Distribution
st.subheader("Primary Type Distribution")
st.bar_chart(filtered['TYPE1'].value_counts())

# Scatter: Combat Power vs Effectiveness
st.subheader("Combat Power vs Overall Effectiveness")
scatter = alt.Chart(filtered).mark_circle(size=60).encode(
    x='Combat_Power',
    y='Overall_Effectiveness',
    color='TYPE1',
    tooltip=['NAME', 'TYPE1', 'TYPE2', 'Combat_Power', 'Overall_Effectiveness']
).interactive()
st.altair_chart(scatter, use_container_width=True)

# Download button
csv = filtered.to_csv(index=False)
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name='filtered_pokemon.csv',
    mime='text/csv'
)

# Individual Pokémon details
st.write("---")
st.subheader("Pokémon Details")
poke = st.selectbox("Select a Pokémon for details:", filtered['NAME'].unique())
poke_data = df[df['NAME'] == poke]
st.write(poke_data)
