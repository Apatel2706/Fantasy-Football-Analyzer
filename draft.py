import pandas as pd

# Load each position separately
df_qb = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_QB.csv")
df_wr = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_WR.csv")
df_rb = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_RB.csv")
df_te = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_TE.csv")

# Add position label
df_qb["Pos"] = "QB"
df_wr["Pos"] = "WR"
df_rb["Pos"] = "RB"
df_te["Pos"] = "TE"

# Combine all into one DataFrame
df = pd.concat([df_qb, df_wr, df_rb, df_te], ignore_index=True)

# Clean and convert stat columns
cols_to_convert = ['YDS', 'TD', 'YDS.1', 'TD.1', 'REC']  # REC is only for WR/RB/TE
for col in cols_to_convert:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)
    else:
        df[col] = 0  # if the column doesn't exist (e.g. REC for QBs), add it as 0

# Define PPR scoring
def calculate_ppr(row):
    return (
        row['YDS'] * 0.1 +     # Receiving or rushing yards
        row['TD'] * 6 +        # Receiving or rushing TDs
        row['YDS.1'] * 0.1 +   # Rushing yards
        row['TD.1'] * 6 +      # Rushing TDs
        row['REC'] * 1         # Receptions
        + (row['Pos'] == 'QB') * (row['YDS'] * -0.06 + row['TD'] * -2)  # Cancel RB/WR scoring on QBs
        + (row['Pos'] == 'QB') * (row['YDS'] * 0.04 + row['TD'] * 4)    # Add QB scoring
    )

# Apply scoring
df['Proj_Pts'] = df.apply(calculate_ppr, axis=1)

# Show top 50 players overall
df_sorted = df[['Player', 'Pos', 'Proj_Pts']].sort_values(by='Proj_Pts', ascending=False)
print(df_sorted.to_string(index=False))
