import pandas as pd

# === Load each position file ===
df_qb = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_QB.csv")
df_wr = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_WR.csv")
df_rb = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_RB.csv")
df_te = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_TE.csv")

# === Add position labels ===
df_qb["Pos"] = "QB"
df_wr["Pos"] = "WR"
df_rb["Pos"] = "RB"
df_te["Pos"] = "TE"

# === Combine all into one big DataFrame ===
df = pd.concat([df_qb, df_wr, df_rb, df_te], ignore_index=True)

# === Clean stat columns ===
cols_to_convert = ['YDS', 'TD', 'YDS.1', 'TD.1', 'REC']
for col in cols_to_convert:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[col] = 0

# === PPR Scoring System ===
def calculate_points(row):
    if row['Pos'] == 'QB':
        return (
            row['YDS'] * 0.04 +      # Passing Yards
            row['TD'] * 4 +          # Passing TDs
            row['YDS.1'] * 0.1 +     # Rushing Yards
            row['TD.1'] * 6          # Rushing TDs
        )
    else:
        return (
            row['YDS'] * 0.1 +       # Receiving or Rushing Yards
            row['TD'] * 6 +          # Receiving or Rushing TDs
            row['YDS.1'] * 0.1 +     # Rushing Yards
            row['TD.1'] * 6 +        # Rushing TDs
            row['REC'] * 1           # Receptions
        )

# === Apply scoring ===
df['Points'] = df.apply(calculate_points, axis=1)

# === Tier Function ===
def assign_tiers(position_df, num_tiers=4):
    position_df = position_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    total = len(position_df)

    if total < num_tiers:
        position_df['Tier'] = [f"Tier {i+1}" for i in range(total)]
    else:
        size = total // num_tiers
        extra = total % num_tiers
        tiers = []
        start = 0
        for i in range(1, num_tiers + 1):
            end = start + size + (1 if i <= extra else 0)
            tiers.extend([f"Tier {i}"] * (end - start))
            start = end
        position_df['Tier'] = tiers

    return position_df

# === Apply tiers by position ===
df_qb = assign_tiers(df[df['Pos'] == 'QB'])
df_wr = assign_tiers(df[df['Pos'] == 'WR'])
df_rb = assign_tiers(df[df['Pos'] == 'RB'])
df_te = assign_tiers(df[df['Pos'] == 'TE'])

# === Filter tiers ===
df_qb = df_qb[df_qb['Tier'].isin(['Tier 1', 'Tier 2'])]  # Only Tier 1–2 for QBs
df_wr = df_wr[df_wr['Tier'].isin(['Tier 1', 'Tier 2', 'Tier 3'])]
df_rb = df_rb[df_rb['Tier'].isin(['Tier 1', 'Tier 2', 'Tier 3'])]
df_te = df_te[df_te['Tier'].isin(['Tier 1', 'Tier 2', 'Tier 3'])]


# === Show each group ===
print("\n=== Quarterbacks (QB) ===")
print(df_qb[['Player', 'Points', 'Tier']].sort_values(by=['Tier', 'Points'], ascending=[True, False]).to_string(index=False))

print("\n=== Wide Receivers (WR) ===")
print(df_wr[['Player', 'Points', 'Tier']].sort_values(by=['Tier', 'Points'], ascending=[True, False]).to_string(index=False))

print("\n=== Running Backs (RB) ===")
print(df_rb[['Player', 'Points', 'Tier']].sort_values(by=['Tier', 'Points'], ascending=[True, False]).to_string(index=False))

print("\n=== Tight Ends (TE) ===")
print(df_te[['Player', 'Points', 'Tier']].sort_values(by=['Tier', 'Points'], ascending=[True, False]).to_string(index=False))
