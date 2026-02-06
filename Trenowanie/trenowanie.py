import pandas as pd
import numpy as np
import optuna
import joblib
from sqlalchemy import create_engine
from xgboost import XGBClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- 1. KONFIGURACJA BAZY DANYCH ---
DB_USER = 'root'
DB_PASSWORD = 'MariaDB'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'liga'

connection_str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_str)

# --- 2. POBIERANIE DANYCH ---

sql_games = """
SELECT 
    win_top_player_id, win_jungle_player_id, win_mid_player_id, win_bot_player_id, win_support_player_id,
    lost_top_player_id, lost_jungle_player_id, lost_mid_player_id, lost_bot_player_id, lost_support_player_id
FROM game_data
"""
df_games = pd.read_sql(sql_games, engine)

sql_players = """
SELECT id, champion, gold_earned, gold_per_minute
FROM player_game_info 
WHERE game_mode = 'CLASSIC' OR game_mode = 'RANKED'
"""
df_players = pd.read_sql(sql_players, engine)

# --- 3. FILTROWANIE KRÓTKICH GIER ---

df_players = df_players[df_players['gold_per_minute'] > 0]

df_players['duration_minutes'] = df_players['gold_earned'] / df_players['gold_per_minute']

valid_players = df_players[df_players['duration_minutes'] > 16]

id_to_champ = valid_players.set_index('id')['champion'].to_dict()

# --- 4. TWORZENIE CECH Z PODZIAŁEM NA ROLE ---

def map_row_with_roles(row):
    try:
        return [
            # WIN TEAM
            f"TOP_{id_to_champ[row['win_top_player_id']]}",
            f"JNG_{id_to_champ[row['win_jungle_player_id']]}",
            f"MID_{id_to_champ[row['win_mid_player_id']]}",
            f"BOT_{id_to_champ[row['win_bot_player_id']]}",
            f"SUP_{id_to_champ[row['win_support_player_id']]}",
            # LOST TEAM
            f"TOP_{id_to_champ[row['lost_top_player_id']]}",
            f"JNG_{id_to_champ[row['lost_jungle_player_id']]}",
            f"MID_{id_to_champ[row['lost_mid_player_id']]}",
            f"BOT_{id_to_champ[row['lost_bot_player_id']]}",
            f"SUP_{id_to_champ[row['lost_support_player_id']]}"
        ]
    except KeyError:
        return None

match_data = df_games.apply(map_row_with_roles, axis=1, result_type='expand')

match_data = match_data.dropna()
match_data.columns = ['W_TOP', 'W_JNG', 'W_MID', 'W_BOT', 'W_SUP', 
                      'L_TOP', 'L_JNG', 'L_MID', 'L_BOT', 'L_SUP']

print(f"   Liczba meczów do nauki: {len(match_data)}")

# --- 5. KODOWANIE ---

mlb = MultiLabelBinarizer()
all_tokens = pd.unique(match_data.values.ravel())
mlb.fit([all_tokens])

def create_dataset(team1_df, team2_df):
    t1_matrix = mlb.transform(team1_df.values)
    t2_matrix = mlb.transform(team2_df.values)
    return np.hstack([t1_matrix, t2_matrix])

X_win = create_dataset(
    match_data[['W_TOP', 'W_JNG', 'W_MID', 'W_BOT', 'W_SUP']],
    match_data[['L_TOP', 'L_JNG', 'L_MID', 'L_BOT', 'L_SUP']]
)
y_win = np.ones(len(X_win))

X_loss = create_dataset(
    match_data[['L_TOP', 'L_JNG', 'L_MID', 'L_BOT', 'L_SUP']],
    match_data[['W_TOP', 'W_JNG', 'W_MID', 'W_BOT', 'W_SUP']]
)
y_loss = np.zeros(len(X_loss))

X = np.vstack([X_win, X_loss])
y = np.concatenate([y_win, y_loss])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# --- 6. OPTYMALIZACJA PARAMETRÓW (OPTUNA) ---

def objective(trial):
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 200, 800),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 5),
        
        'n_jobs': -1,
        'eval_metric': 'logloss',
        'random_state': 42,
        'verbosity': 0
    }
    
    model = XGBClassifier(**param)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    
    return accuracy

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print("Najlepsze parametry:")
print(study.best_params)
print(f"Najlepsza osiągnięta dokładność w testach: {study.best_value*100:.2f}%")

# --- 7. TRENING FINALNY I ZAPIS ---

best_params = study.best_params
best_params['n_jobs'] = -1
best_params['eval_metric'] = 'logloss'
best_params['random_state'] = 42

final_model = XGBClassifier(**best_params)
final_model.fit(X_train, y_train)

final_acc = final_model.score(X_test, y_test)
print(f"Finalna dokładność zapisanego modelu: {final_acc*100:.2f}%")

joblib.dump(final_model, 'lol_model.pkl')
joblib.dump(mlb, 'lol_encoder.pkl')

print("GOTOWE!")