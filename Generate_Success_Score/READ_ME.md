# F1 Race Success Score Pipeline

This project calculates a machine learning-based "success score" for F1 drivers based on estimated finish times and other performance metrics from historical race data (1999–2024).

---

## Pipeline Overview

### Step 1: Manually Export CSVs from Snowflake

Export the following tables from Snowflake using the SQL queries saved in `Generate_Success_Score/sql_queries/`, and save them as CSV files in `Generate_Success_Score/csv_files/`.

**Required CSVs:**

- `01_race_results_1999_2024_clean`
- `02_lap_times_1999_2024`

These will be used as inputs in the subsequent processing steps.

---

### Step 2: Calculate Total Lap Finish Times

**Script:** `python_scripts/add_lap_times.py`

- Cleans and standardises lap time strings (removing any `hh:` prefix)
- Converts lap times to `timedelta` objects
- Aggregates per driver per race to compute total race time

**Output:** `driver_finish_times_1999_2024.csv`

---

### Step 3: Merge Lap Finish Times with Race Results

**Script:** `python_scripts/merge_finish_times.py`

- Loads the driver lap summary (from Step 2) and the main race results table
- Merges the two datasets on `RACEID` and `DRIVERID` using a left join
- Appends total race time columns (`FINISH_TIME_INT_SEC`, `FINISH_TIME_STR`) to each driver's result

**Output:** `race_results_1999_2024_with_finish_times.csv`

---

### Step 4: Estimate Finish Times for Incomplete Drivers

**Script:** `python_scripts/estimate_finish_times.py`

- Loads merged race results with recorded lap times (from Step 3)
- Identifies the maximum number of laps completed per race
- Calculates how many laps each driver was behind the winner (`laps_behind`)
- Estimates total race time for:
  - **Lapped drivers**, using their average lap time, adjusted with a 3% penalty per missing lap
  - **DNF (Did Not Finish) drivers** who completed at least 1 lap, using the same method and an additional 5% penalty for incompletion
- Converts estimated times to seconds and formats them for readability

**Output:** `race_results_1999_2024_with_estimated_times.csv`

---

### Step 5: Clean and Organise the Estimated Times Table

**Script:** `python_scripts/clean_estimated_times.py`

- Loads the enriched dataset from Step 4
- Removes the original raw finish time columns:
  - `FINISH_TIME_INT_SEC`
  - `FINISH_TIME_STR`
- Reorders the remaining columns for logical readability, placing the most important race metrics and estimated times up front
- Ensures that unexpected or extra columns are retained at the end of the dataset

**Output:** `race_results_1999_2024_cleaned_with_estimated_times.csv`

---

### Step 6: Generate Machine Learning Success Scores

**Script:** `python_scripts/generate_success_scores.py`  
**Output:** `race_results_1999_2024_with_success_score.csv`

#### How It Works

This script uses **LightGBM**, a high-performance gradient boosting framework, to generate a success score for every driver in every race. The goal is to quantify not just who finished where, but how well they performed relative to their peers using more nuanced race metrics.

#### Step-by-Step Breakdown

##### Feature Selection

The model uses the following performance indicators:

- `GRID` — Starting grid position
- `LAPS` — Laps completed
- `FASTESTLAPSPEED` — Top lap speed
- `ESTIMATED_FINISH_TIME` — Final time including adjustments for lapped/DNF drivers

Missing values are filled with `0` to avoid crashes or NaNs during training.

##### Ranking Labels

Drivers are ranked by `ESTIMATED_FINISH_TIME` per race (lower time = better performance). These ranks are used as training labels for the model.

##### Model Training

A **LightGBM LambdaRank** model is trained using:

- Objective: `'lambdarank'` (for learning pairwise ranking)
- Metric: `'ndcg'` (normalised discounted cumulative gain)
- Grouping: By `RACEID`, so the model learns within each race context

This means the model doesn't just learn "what's fast" but rather "what's fast in this specific race".

##### Score Prediction

After training, the model outputs a raw `ML_SCORE` for each driver, indicating how "strong" their performance was.

##### Hybrid Success Score Calculation

A hybrid system blends:

- Raw finishing order (linear scale from 100 to 0)
- Model-inferred quality (`ML_SCORE`, scaled using `MinMaxScaler` from 0.8 to 1.2)

The final score is calculated like so:

```python
SUCCESS_SCORE = BASE_ORDERED_SCORE × ML_INFLUENCE
```

To prevent illogical results (e.g. someone behind outscoring someone ahead), the algorithm enforces strict descending order, subtracting small penalties if needed.

#### Final Cleanup

- Drops training artefacts like `ML_SCORE`, `ML_INFLUENCE`, and `RANK`
- Exports the final table with:
  - Race and driver metadata
  - Estimated finish metrics
  - `ML_SUCCESS_SCORE`: the final polished ranking metric

---

### Step 7: View and Explore the Success Scores

**Script:** `python_scripts/view_success_score_table.py`  
**Command to run:**

```bash
streamlit run Generate_Success_Score/python_scripts/view_success_score_table.py
```

#### What It Does

This tool allows you to explore and analyse the final success scores in an intuitive, interactive table:

- Select a race from the sidebar dropdown
- Choose which columns to display (e.g. driver, laps, final time, success score)
- View sorted results by success score (descending), helping you quickly spot standout performances or anomalies

---

## Summary

This pipeline combines SQL data extraction, pandas based data cleaning and aggregation, and a LightGBM machine learning model to generate a hybrid success metric for every F1 race from 1999 to 2024. It is modular, transparent, and designed for exploratory analysis as well as model refinement.

You can rerun any step individually or modify it to introduce alternative scoring strategies or visualisations.
