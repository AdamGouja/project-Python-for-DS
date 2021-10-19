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

def add_country(df):
    country = []
    for elements in df["League"] :
        if elements == "LCK" :
            country.append("Korea")
        elif elements == "NALCS" :
            country.append("North America")
        elif elements == "EULCS" :
            country.append("Europe")
        elif elements == "CBLoL" :
            country.append("Brazil")
        elif elements == "TCL" :
            country.append("North America")
        else :
            country.append("not found")
    df.insert(1, "Country", country)

df = pd.read_csv("data/LeagueofLegends.csv")
df_gold_length = new_df_gold_length(df)
add_country(df_gold_length)
print(df_gold_length.head())