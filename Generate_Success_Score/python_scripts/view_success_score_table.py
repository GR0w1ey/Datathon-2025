import streamlit as st
import pandas as pd

# Load the CSV
df = pd.read_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_success_score.csv")

st.title("F1 Success Score Viewer")

# Detect all available columns
all_columns = df.columns.tolist()

# Sidebar: Select Race
race_ids = df['RACEID'].unique()
selected_race = st.sidebar.selectbox("Select Race", sorted(race_ids))

# Sidebar: Column Selection with safe default
default_cols = [col for col in [
    'DRIVERID', 'LAPS', 'POSITION',
    'ESTIMATED_FINISH_TIME_STR', 'ML_SUCCESS_SCORE', 'STATUS'
] if col in all_columns]

selected_cols = st.sidebar.multiselect(
    "Columns to Display",
    options=all_columns,
    default=default_cols
)

# Filter and show table
filtered_df = df[df['RACEID'] == selected_race]

if selected_cols:
    st.dataframe(filtered_df[selected_cols].sort_values(by='ML_SUCCESS_SCORE', ascending=False))
else:
    st.warning("Please select at least one column to display.")


# Use below in terminal to view table
# streamlit run Generate_Success_Score/python_scripts/success_score_utils.py

