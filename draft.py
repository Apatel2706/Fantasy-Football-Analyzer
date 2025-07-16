import pandas as pd

# Load CSV
df = pd.read_csv("FantasyPros_Fantasy_Football_Statistics_QB.csv")

# Convert relevant columns to numbers
cols_to_convert = ['YDS', 'TD', 'YDS.1', 'TD.1']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Scoring function
def calculate_ppr(row):
    return (
        row['YDS'] * 0.04 +     # Passing Yards
        row['TD'] * 4 +         # Passing TDs
        row['YDS.1'] * 0.1 +    # Rushing Yards
        row['TD.1'] * 6         # Rushing TDs
    )

# Apply scoring
df['Proj_Pts'] = df.apply(calculate_ppr, axis=1)

# Show top 10
print(df[['Player', 'Proj_Pts']].sort_values(by='Proj_Pts', ascending=False).head(10))

