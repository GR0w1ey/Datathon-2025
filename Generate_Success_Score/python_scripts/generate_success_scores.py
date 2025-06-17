import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler

def generate_success_scores():
    df = pd.read_csv("csv_files/race_results_2024_cleaned_with_estimated_times.csv")

    # Prep
    df['ESTIMATED_FINISH_TIME'] = pd.to_numeric(df['ESTIMATED_FINISH_TIME'], errors='coerce')
    df = df[df['ESTIMATED_FINISH_TIME'].notnull()]
    df['ESTIMATED_FINISH_TIME_STR'] = pd.to_timedelta(df['ESTIMATED_FINISH_TIME'], unit='s').astype(str).str.replace("0 days ", "", regex=False)

    # Features to feed to ML
    features = ['GRID', 'POINTS', 'LAPS', 'FASTESTLAPSPEED', 'ESTIMATED_FINISH_TIME']
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

    # --- Hybrid Scoring: ML + Finish Order ---
    def compute_final_score(group):
        group = group.sort_values('ESTIMATED_FINISH_TIME').reset_index(drop=True)

        # ML ranking influence
        scaler = MinMaxScaler(feature_range=(0.8, 1.2))
        group['ML_INFLUENCE'] = scaler.fit_transform(group['ML_SCORE'].values.reshape(-1, 1))

        # Base score based strictly on finishing order
        n = len(group)
        base_scores = np.linspace(100, 40, num=n)  # hard-coded descending line
        group['ML_SUCCESS_SCORE'] = base_scores * group['ML_INFLUENCE']

        # Re-enforce strict order so no one scores higher than someone ahead
        for i in range(1, len(group)):
            if group.loc[i, 'ML_SUCCESS_SCORE'] > group.loc[i - 1, 'ML_SUCCESS_SCORE']:
                group.loc[i, 'ML_SUCCESS_SCORE'] = group.loc[i - 1, 'ML_SUCCESS_SCORE'] - 0.01

        group['ML_SUCCESS_SCORE'] = group['ML_SUCCESS_SCORE'].clip(lower=0).round(2)
        return group

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
    df.to_csv("csv_files/race_results_2024_with_success_score.csv", index=False)
