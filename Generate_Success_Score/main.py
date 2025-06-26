from python_scripts.success_score_utils import success_score_utils

def main():
    print("Step 1: Run SQL Queries to get CSV files...\n")
    # Cba figuring out how to use snowflake connector

    print("Step 2: Calculating total lap finish times...\n")
    success_score_utils.add_lap_times()

    print("Step 3: Merging the finish times...\n")
    success_score_utils.merge_finish_times()

    print("Step 4: Estimating the finish times...\n")
    success_score_utils.estimate_finish_times()

    print("Step 5: Cleaning the table...\n")
    success_score_utils.clean_estimated_times()
    
    print("Step 6: Calculating the success score...\n")
    success_score_utils. generate_success_scores()

    print("\nAll steps completed successfully.\n")

if __name__ == "__main__":
    main()
