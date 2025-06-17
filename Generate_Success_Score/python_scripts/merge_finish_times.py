import pandas as pd

def merge_finish_times():
    # Load your files
    lap_summary_df = pd.read_csv("Generate_Success_Score/csv_files/driver_finish_times_2024.csv")  # the one with FINISH_TIME
    results_df = pd.read_csv("Generate_Success_Score/csv_files/01_race_results_2024_clean.csv")       # your main result table

    # Merge on RACEID and DRIVERID
    merged_df = pd.merge(results_df, lap_summary_df, on=["RACEID", "DRIVERID"], how="left")

    # Save to new CSV
    merged_df.to_csv("Generate_Success_Score/csv_files/race_results_2024_with_finish_times.csv", index=False)

    # Optional: preview merged data
    # print(merged_df.head())
