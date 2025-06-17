import pandas as pd

def estimate_finish_times():
    # Load the dataset
    df = pd.read_csv("csv_files/race_results_2024_with_finish_times.csv")

    # Convert FINISH_TIME_INT_SEC to float seconds
    df['FINISH_TIME_INT_SEC'] = pd.to_timedelta(df['FINISH_TIME_INT_SEC']).dt.total_seconds()

    # Get max laps per race
    max_laps = df.groupby('RACEID')['LAPS'].max()
    df = df.merge(max_laps.rename('MAX_LAPS'), on='RACEID')
    
    # Calculate laps behind
    laps_behind = df['MAX_LAPS'] - df['LAPS']

    # Copy the original finish time to start
    df['ESTIMATED_FINISH_TIME'] = df['FINISH_TIME_INT_SEC']

    # Lapped drivers ("+1 Lap", "+2 Laps", etc.)
    lapped = df['STATUS'].str.match(r'^\+\d+ Lap')
    df.loc[lapped, 'ESTIMATED_FINISH_TIME'] = (
        df.loc[lapped, 'FINISH_TIME_INT_SEC'] * (1 + 0.03 * laps_behind[lapped])
    )

    # DNF drivers who completed at least 1 lap
    dnf = ~df['STATUS'].str.match(r'^(Finished|\+\d+ Lap)') & (df['LAPS'] > 0)
    df.loc[dnf, 'ESTIMATED_FINISH_TIME'] = (
        df.loc[dnf, 'FINISH_TIME_INT_SEC'] * (1 + 0.03 * laps_behind[dnf] + 0.05)
    )

    # Round and convert to string format
    df['ESTIMATED_FINISH_TIME'] = df['ESTIMATED_FINISH_TIME'].round(3)
    df['ESTIMATED_FINISH_TIME_STR'] = pd.to_timedelta(df['ESTIMATED_FINISH_TIME'], unit='s').astype(str)

    # Drop temp columns
    df = df.drop(columns=['MAX_LAPS'])

    # Save full table with new columns
    df.to_csv("csv_files/race_results_2024_with_estimated_times.csv", index=False)

    # Preview
    # print(df[['RACEID', 'DRIVERID', 'STATUS', 'ESTIMATED_FINISH_TIME', 'ESTIMATED_FINISH_TIME_STR']].head())
