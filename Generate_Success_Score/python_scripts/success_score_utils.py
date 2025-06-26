import pandas as pd
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler
import streamlit as st

def fix_time_format(time):
    """
    Fix TIME format: if already hh:mm:ss.sss, strip the first hours and keep mm:ss.sss

    Args:
      time (str): Time data as a string.

    Returns:
      str: Time data as a string in hh:mm:ss.sss format.
    """
        split_time = time.split(':')
        minutes = split_time[1]
        seconds = split_time[2]
        # Check if the time is in the correct format.
        if len(parts) == 3:
          # If the time string contains hour data it should be
          # dropped and return the time in mm:ss.sss format.
            return f"{int(minutes):02}:{seconds}"
        # If the time string is already in the mm:ss.sss format
        # return as-is.
        else:
          return time

def add_lap_times():
  """
  Add preprocessed lap times data to race dataset.
  """
    # Load the CSV
    df = pd.read_csv("Generate_Success_Score/csv_files/02_lap_times_1999_2024.csv")

    # Convert all TIME values to string
    df['TIME'] = df['TIME'].astype(str)
    df['TIME'] = df['TIME'].apply(fix_time_format)

    # Check for any remaining invalid formats
    bad_rows = df[~df['TIME'].str.match(r'^\d{1,2}:\d{2}\.\d{3}$', na=False)]

    if not bad_rows.empty:
        print(f"Found {len(bad_rows)} rows with invalid TIME format.")
        print(bad_rows[['RACEID', 'DRIVERID', 'TIME']].head(10))
        print("Script stopped due to invalid TIME values.")

    # Convert TIME to timedelta
    df['LAP_TIME'] = pd.to_timedelta('00:' + df['TIME'])

    # Group by RACEID and DRIVERID
    grouped = df.groupby(['RACEID', 'DRIVERID'])

    # Aggregate
    result = grouped.agg(
        FINISH_TIME_INT_SEC=('LAP_TIME', 'sum'),
        LAPS=('LAP', 'count'),
        POSITION=('POSITION', 'first')
    ).reset_index()

    # Convert to float seconds
    result['FINISH_TIME_SECONDS'] = result['FINISH_TIME_INT_SEC'].dt.total_seconds()

    # Format time as HH:MM:SS.sss string
    result['FINISH_TIME_STR'] = result['FINISH_TIME_INT_SEC'].apply(lambda x: str(x).split(' days ')[-1])

    # Final tidy-up and sort
    final = result[['RACEID', 'DRIVERID', 'POSITION', 'FINISH_TIME_INT_SEC', 'FINISH_TIME_STR']]
    final = final.sort_values(by=['RACEID', 'POSITION'])

    # Save to CSV
    final.to_csv("Generate_Success_Score/csv_files/driver_finish_times_1999_2024.csv", index=False)


def clean_estimated_times():
    """
    Clean race results with estimated times data.
    """
    # Load the dataset
    df = pd.read_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_estimated_times.csv")

    # Drop the original finish time columns
    df = df.drop(columns=['FINISH_TIME_INT_SEC', 'FINISH_TIME_STR'])

    # Reorder columns for readability
    column_order = [
        'RACEID', 
        'DRIVERID', 
        'CONSTRUCTORID', 
        'GRID',
        'POSITIONORDER', 
        'POSITION', 
        'POINTS', 
        'STATUSID', 
        'STATUS',
        'LAPS', 
        'FASTESTLAPSPEED', 
        'FASTESTLAPTIME',
        'ESTIMATED_FINISH_TIME', 
        'ESTIMATED_FINISH_TIME_STR'
    ]

    # Apply the column order (keep any unexpected columns at the end)
    ordered_cols = [col for col in column_order if col in df.columns] + [col for col in df.columns if col not in column_order]
    df = df[ordered_cols]

    # Save to new CSV
    df.to_csv("Generate_Success_Score/csv_files/race_results_1999_2024_cleaned_with_estimated_times.csv", index=False)


def estimate_finish_times():
    """
    Calculate estimated finish times.
    """
    # Load the dataset
    df = pd.read_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_finish_times.csv")

    # Convert FINISH_TIME_INT_SEC to float seconds
    df['FINISH_TIME_INT_SEC'] = pd.to_timedelta(df['FINISH_TIME_INT_SEC']).dt.total_seconds()

    # Get max laps per race
    max_laps = df.groupby('RACEID')['LAPS'].max()
    df = df.merge(max_laps.rename('MAX_LAPS'), on='RACEID')
    
    # Calculate laps behind
    laps_behind = df['MAX_LAPS'] - df['LAPS']

    # Copy the original finish time to start
    df['ESTIMATED_FINISH_TIME'] = df['FINISH_TIME_INT_SEC']

    # Estimate average lap time
    df['AVG_LAP_TIME'] = df['FINISH_TIME_INT_SEC'] / df['LAPS']

    # Lapped drivers ("+1 Lap", "+2 Laps", etc.)
    lapped = df['STATUS'].str.match(r'^\+\d+ Lap')
    df.loc[lapped, 'ESTIMATED_FINISH_TIME'] = (
        df.loc[lapped, 'FINISH_TIME_INT_SEC'] * (1 + 0.03 * laps_behind[lapped])
    )

    # Apply full-race estimation + penalty
    df.loc[lapped, 'ESTIMATED_FINISH_TIME'] = (
    df.loc[lapped, 'AVG_LAP_TIME'] * df.loc[lapped, 'MAX_LAPS'] * (1 + 0.03 * laps_behind[lapped] + 0.05)
    )

    # DNF drivers who completed at least 1 lap
    lapped_penalty = 0.03
    dnf = ~df['STATUS'].str.match(r'^(Finished|\+\d+ Lap)') & (df['LAPS'] > 0)
    df.loc[dnf, 'ESTIMATED_FINISH_TIME'] = (
        df.loc[dnf, 'FINISH_TIME_INT_SEC'] * (1 + lapped_penalty * laps_behind[dnf])
    )

    # Apply full-race estimation + penalty
    dnf_penalty = 0.05
    df.loc[dnf, 'ESTIMATED_FINISH_TIME'] = (
    df.loc[dnf, 'AVG_LAP_TIME'] * df.loc[dnf, 'MAX_LAPS'] * (1 + dnf_penalty * laps_behind[dnf])
    )

    # Round and convert to string format
    df['ESTIMATED_FINISH_TIME'] = df['ESTIMATED_FINISH_TIME'].round(3)
    df['ESTIMATED_FINISH_TIME_STR'] = pd.to_timedelta(df['ESTIMATED_FINISH_TIME'], unit='s').astype(str)

    # Drop temp columns
    df = df.drop(columns=['MAX_LAPS'])

    # Save full table with new columns
    df.to_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_estimated_times.csv", index=False)

def compute_final_score(group):
    """
    Compute final scores for drivers using estimated finish times preprocessed
    on a Min-Max Scale.

    Args:
      group (Pandas DataFrame): Race data

    Returns:
      Pandas DataFrame: Race data with final score added as a new column.
    """
    group = group.sort_values('ESTIMATED_FINISH_TIME').reset_index(drop=True)

    # ML ranking influence
    scaler = MinMaxScaler(feature_range=(0.8, 1.2))
    group['ML_INFLUENCE'] = scaler.fit_transform(group['ML_SCORE'].values.reshape(-1, 1))

    # Base score based strictly on finishing order
    n = len(group)
    base_scores = np.linspace(100, 0, num=n)  # hard-coded descending line
    group['ML_SUCCESS_SCORE'] = base_scores * group['ML_INFLUENCE']

    # Re-enforce strict order so no one scores higher than someone ahead
    for i in range(1, len(group)):
        if group.loc[i, 'ML_SUCCESS_SCORE'] > group.loc[i - 1, 'ML_SUCCESS_SCORE']:
            group.loc[i, 'ML_SUCCESS_SCORE'] = group.loc[i - 1, 'ML_SUCCESS_SCORE'] - 0.01

    group['ML_SUCCESS_SCORE'] = group['ML_SUCCESS_SCORE'].clip(lower=0).round(2)
    return group


def generate_success_scores():
    """
    Calculate success scores for drivers using a decision tree trained on:
      -Grid Position
      -Laps
      -Fastest Lap Speed
      -Estimated Finish Time
    """
    df = pd.read_csv("Generate_Success_Score/csv_files/race_results_1999_2024_cleaned_with_estimated_times.csv")

    # Preprocess race results data ahead of training decision tree.
    df['ESTIMATED_FINISH_TIME'] = pd.to_numeric(df['ESTIMATED_FINISH_TIME'], errors='coerce')
    df = df[df['ESTIMATED_FINISH_TIME'].notnull()]
    df['ESTIMATED_FINISH_TIME_STR'] = pd.to_timedelta(df['ESTIMATED_FINISH_TIME'], unit='s').astype(str).str.replace("0 days ", "", regex=False)

    # Features to feed to ML
    features = ['GRID', 'LAPS', 'FASTESTLAPSPEED', 'ESTIMATED_FINISH_TIME']
    df[features] = df[features].fillna(0)

    # Define ranking label based on true finish order
    df['RANK'] = df.groupby('RACEID')['ESTIMATED_FINISH_TIME'].rank(method='first', ascending=True).astype(int)

    # Prepare LightGBM data
    X = df[features]
    y = df['RANK']
    group_sizes = df.groupby('RACEID').size().values
    train_data = lgb.Dataset(X, label=y, group=group_sizes)

    # Train model
    params = {
        'objective': 'lambdarank',
        'metric': 'ndcg',
        'learning_rate': 0.1,
        'num_leaves': 31,
        'verbosity': -1
    }

    model = lgb.train(params, train_data, num_boost_round=100)
    df['ML_SCORE'] = model.predict(X)

    df = df.groupby('RACEID', group_keys=False).apply(compute_final_score)

    # Final export cleanup
    drop_cols = ['ML_SCORE', 'ML_INFLUENCE', 'RANK']
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

    col_order = [
        'RACEID', 'DRIVERID', 'CONSTRUCTORID', 'GRID', 'POSITIONORDER', 'POSITION',
        'POINTS', 'STATUSID', 'STATUS', 'LAPS', 'FASTESTLAPSPEED', 'FASTESTLAPTIME',
        'ESTIMATED_FINISH_TIME', 'ESTIMATED_FINISH_TIME_STR', 'ML_SUCCESS_SCORE'
    ]
    df = df[[col for col in col_order if col in df.columns]]
    df.to_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_success_score.csv", index=False)


def merge_finish_times():
    """
    Merge the main race results dataset with the finish times data.
    """
    # Load your files
    lap_summary_df = pd.read_csv("Generate_Success_Score/csv_files/driver_finish_times_1999_2024.csv")  # the one with FINISH_TIME
    results_df = pd.read_csv("Generate_Success_Score/csv_files/01_race_results_1999_2024_clean.csv")       # your main result table

    # Merge on RACEID and DRIVERID
    merged_df = pd.merge(results_df, lap_summary_df, on=["RACEID", "DRIVERID"], how="left")

    # Save to new CSV
    merged_df.to_csv("Generate_Success_Score/csv_files/race_results_1999_2024_with_finish_times.csv", index=False)


def view view_success_score_table():
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
    # streamlit run Generate_Success_Score/python_scripts/view_success_score_table.py
