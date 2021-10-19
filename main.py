import pandas as pd

def new_df_gold_length(df):
    df2 = df[['League', 'Type','blueTeamTag','bResult','rResult','redTeamTag','gamelength','golddiff']]

    df2=df2[(df2['League'] == 'NALCS') | 
            (df2['League'] == 'LCK') | 
            (df2['League'] == 'EULCS') |
            (df2['League'] == 'TCL') |
            (df2['League'] == 'CBLoL')]
    df2= df2[(df2['Type'] != 'Regional') & (df2['Type'] != 'Promotion')]

    return df2

df = pd.read_csv("data/LeagueofLegends.csv")
df_gold_length = new_df_gold_length(df)
#print(df2['Type'].unique())
print(df_gold_length['redTeamTag'].isna().value_counts())