from python_scripts.add_lap_times import add_lap_times
from python_scripts.merge_finish_times import merge_finish_times
from python_scripts.estimate_finish_times import estimate_finish_times
from python_scripts.clean_estimated_times import clean_estimated_times
from python_scripts.generate_success_scores import generate_success_scores

def main():
    print("Step 1: Run SQL Queries to get CSV files...\n")
    # Cba figuring out how to use snowflake connector

    print("Step 2: Calculating total lap finish times...\n")
    add_lap_times()

    print("Step 3: Merging the finish times...\n")
    merge_finish_times()

    print("Step 4: Estimating the finish times...\n")
    estimate_finish_times()

    print("Step 5: Cleaning the table...\n")
    clean_estimated_times()
    
    print("Step 6: Calculating the success score...\n")
    generate_success_scores()

    print("\nAll steps completed successfully.\n")

if __name__ == "__main__":
    main()
