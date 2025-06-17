import pandas as pd

def add_lap_times():
    # Load the CSV
    df = pd.read_csv("Generate_Success_Score/csv_files/02_lap_times_2024.csv")

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
    final.to_csv("Generate_Success_Score/csv_files/driver_finish_times_2024.csv", index=False)

    # Optional preview
    # print(final.head())
