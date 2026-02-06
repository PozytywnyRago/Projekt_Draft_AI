import joblib
import numpy as np
import os
import sys
import difflib
from role import NORMALIZED_WHITELIST

# --- KONFIGURACJA ---
MODEL_FILE = 'lol_model.pkl'
ENCODER_FILE = 'lol_encoder.pkl'

ROLES = ['TOP', 'JNG', 'MID', 'BOT', 'SUP']
ROLE_NAMES_PL = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']

# --- 1. ŁADOWANIE ---
if not os.path.exists(MODEL_FILE) or not os.path.exists(ENCODER_FILE):
    print(f"BŁĄD: Brak pliku modelu.")
    sys.exit()

model = joblib.load(MODEL_FILE)
mlb = joblib.load(ENCODER_FILE)

all_tokens = mlb.classes_
valid_champion_names_db = set()
for token in all_tokens:
    if '_' in token:
        valid_champion_names_db.add(token.split('_', 1)[1])

lower_to_correct = {name.lower(): name for name in valid_champion_names_db}

# --- 2. FUNKCJE POMOCNICZE ---

def get_valid_input(prompt, allow_empty=True):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            if allow_empty: return None
            else: 
                print("To pole nie może być puste.")
                continue

        user_lower = user_input.lower()
        if user_lower in lower_to_correct:
            return lower_to_correct[user_lower]
        
        print(f"Błąd w nazwie postaci: '{user_input}'.")
        closest = difflib.get_close_matches(user_input, valid_champion_names_db, n=3, cutoff=0.6)
        if closest: print(f"   Czy chodziło Ci o: {', '.join(closest)}?")

def build_feature_vector(my_team_dict, enemy_team_dict, candidate_champ=None, candidate_role=None):
    tokens = []
    
    for role in ROLES:
        champ = my_team_dict.get(role)
        if role == candidate_role and candidate_champ:
            tokens.append(f"{role}_{candidate_champ}")
        elif champ:
            tokens.append(f"{role}_{champ}")
            
    enemy_tokens = []
    for role in ROLES:
        champ = enemy_team_dict.get(role)
        if champ:
            enemy_tokens.append(f"{role}_{champ}")
            
    vec_my = mlb.transform([tokens])
    vec_enemy = mlb.transform([enemy_tokens])
    return np.hstack([vec_my, vec_enemy])

# --- 3. GŁÓWNA PĘTLA APLIKACJI ---

def run_app():
    print("\n" + "="*60)
    print("   LEAGUE OF LEGENDS - DRAFT AI")
    print("="*60)
    
    while True:
        print("\n--- NOWY DRAFT ---")
        
        print("Na jakiej pozycji grasz?")
        for i, role_pl in enumerate(ROLE_NAMES_PL):
            print(f"{i+1}. {role_pl}")
            
        try:
            choice = input("Wybór (1-5): ").strip()
            if choice not in ['1','2','3','4','5']: continue
            target_role_idx = int(choice) - 1
            target_role_code = ROLES[target_role_idx]
        except: continue

        my_team = {}
        enemy_team = {}
        used_champions = set()

        print(f"\n--- SOJUSZNICY (Szukamy: {ROLE_NAMES_PL[target_role_idx]}) ---")
        for i, role_code in enumerate(ROLES):
            if i == target_role_idx: continue
            champ = get_valid_input(f"Sojusznik na pozycji {ROLE_NAMES_PL[i]}: ")
            if champ: 
                my_team[role_code] = champ
                used_champions.add(champ)

        print("\n--- PRZECIWNICY ---")
        for i, role_code in enumerate(ROLES):
            champ = get_valid_input(f"Przeciwnik na pozycji {ROLE_NAMES_PL[i]}: ")
            if champ: 
                enemy_team[role_code] = champ
                used_champions.add(champ)
        
        suggestions = []
        
        allowed_champs = NORMALIZED_WHITELIST.get(target_role_code, set())
        
        if not allowed_champs:
            print(f"Pusta lista w role.py dla {target_role_code}!")
        
        for champ_name in allowed_champs:
            if champ_name in used_champions:
                continue
                
            token_check = f"{target_role_code}_{champ_name}"
            if token_check not in mlb.classes_:
                continue

            input_vec = build_feature_vector(my_team, enemy_team, champ_name, target_role_code)
            win_prob = model.predict_proba(input_vec)[0][1]
            suggestions.append((champ_name, win_prob))
            
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n TOP 5 - {ROLE_NAMES_PL[target_role_idx]}:")
        print("-" * 40)
        
        if not suggestions:
            print("Brak sugestii.")
        
        for i, (name, prob) in enumerate(suggestions[:5], 1):
            percent = prob * 100         
            print(f"{i}. {name:<15} {percent:.2f}%")
            
        input("\n[ENTER] - Nowy draft")

if __name__ == "__main__":
    try: run_app()
    except KeyboardInterrupt: print("\nZakończono.")