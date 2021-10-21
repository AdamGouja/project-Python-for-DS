import pandas as pd
import geopy
from geopy.geocoders import Nominatim

def new_df_gold_length(df):
    """
    Crée un nouveau dataframe avec comme colonnes 'League', 'Type','blueTeamTag','bResult','rResult','redTeamTag','gamelength' et 'golddiff'.

    Args:
        df: dataframe initial

    Returns:
        Nouveau dataframe.
    """
    df2 = df[['League', 'Type','blueTeamTag','bResult','rResult','redTeamTag','gamelength','golddiff']]

    df2=df2[(df2['League'] == 'NALCS') | 
            (df2['League'] == 'LCK') | 
            (df2['League'] == 'EULCS') |
            (df2['League'] == 'TCL') |
            (df2['League'] == 'CBLoL')]
    df2= df2[(df2['Type'] != 'Regional') & (df2['Type'] != 'Promotion')]

    return df2

def add_country_localisation(df, position):
    """
    Ajoute une colonne "Country", "Lattitude" et "Longitude" au dataframe mis en argument selon la ligue du match en question.

    Args:
        df : dataframe où ajouter les colonnes
        position : numéro de la colonne à partir de laquelle ajouter les colonnes
    """
    
    app = Nominatim(user_agent="Adam")

    k  = [app.geocode("Korea").raw["lat"], app.geocode("Korea").raw["lon"]]
    na = [app.geocode("North America").raw["lat"], app.geocode("North America").raw["lon"]]
    eu = [app.geocode("Europe").raw["lat"], app.geocode("Europe").raw["lon"]]
    br = [app.geocode("Brazil").raw["lat"], app.geocode("Brazil").raw["lon"]]
    t  = [app.geocode("Turkey").raw["lat"], app.geocode("Turkey").raw["lon"]]

    country = []
    lattitude = []
    longitude = []

    for elements in df["League"] :
        if elements == "LCK" :
            country.append("Korea")
            lattitude.append(k[0])
            longitude.append(k[1])
        elif elements == "NALCS" :
            country.append("North America")
            lattitude.append(na[0])
            longitude.append(na[1])
        elif elements == "EULCS" :
            country.append("Europe")
            lattitude.append(eu[0])
            longitude.append(eu[1])
        elif elements == "CBLoL" :
            country.append("Brazil")
            lattitude.append(br[0])
            longitude.append(br[1])
        elif elements == "TCL" :
            country.append("Turkey")
            lattitude.append(t[0])
            longitude.append(t[1])
        else :
            country.append("not found")
            lattitude.append("not found")
            longitude.append("not found")
    df.insert(position, "Country", country)
    df.insert(position+1, "Lattitude", lattitude)
    df.insert(position+2, "Longitude", longitude)


df = pd.read_csv("data/LeagueofLegends.csv")
df_gold_length = new_df_gold_length(df)

add_country_localisation(df_gold_length,1)

print(df_gold_length.head())
