import pandas as pd

def clean_estimated_times():
    # Load the dataset
    df = pd.read_csv("csv_files/race_results_2024_with_estimated_times.csv")

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
    df.to_csv("csv_files/race_results_2024_cleaned_with_estimated_times.csv", index=False)

    # Preview
    # print(df.head())
