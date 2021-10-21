import pandas as pd
import geopy
from geopy.geocoders import Nominatim
#import time
#from pprint import pprint

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

def add_country(df, position):
    """
    Ajoute une colonne "Country" au dataframe mis en argument selon la ligue du match en question.

    Args:
        df : dataframe où ajouter la colonne
        position : numéro de la colonne où ajouter "Country"
    """
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
            country.append("Turkey")
        else :
            country.append("not found")
    df.insert(position, "Country", country)

def add_localisation(df, position):
    """
    Ajoute une colonne "Lattitude" et une colonne "Longitude au dataframe mis en argument selon le pays de chaque ligue.

    Args:
        df : dataframe où ajouter les colonnes
        position : numéro de la colonne où ajouter la colonne lattitude, la colonne longitude sera posée après
    """
    app = Nominatim(user_agent="Adam")

    k  = [app.geocode("Korea").raw["lat"], app.geocode("Korea").raw["lon"]]
    na = [app.geocode("North America").raw["lat"], app.geocode("North America").raw["lon"]]
    eu = [app.geocode("Europe").raw["lat"], app.geocode("Europe").raw["lon"]]
    br = [app.geocode("Brazil").raw["lat"], app.geocode("Brazil").raw["lon"]]
    t  = [app.geocode("Turkey").raw["lat"], app.geocode("Turkey").raw["lon"]]

    lattitude = []
    longitude = []
    for elements in df["Country"]:
        if elements == "Korea":
            lattitude.append(k[0])
            longitude.append(k[1])
        elif elements == "North America":
            lattitude.append(na[0])
            longitude.append(na[1])
        elif elements == "Europe":
            lattitude.append(eu[0])
            longitude.append(eu[1])
        elif elements == "Brazil":
            lattitude.append(br[0])
            longitude.append(br[1])
        elif elements == "Turkey":
            lattitude.append(t[0])
            longitude.append(t[1])
    df.insert(position, "Lattitude", lattitude)
    df.insert(position+1, "Longitude", longitude)



df = pd.read_csv("data/LeagueofLegends.csv")
df_gold_length = new_df_gold_length(df)
add_country(df_gold_length, 1)
add_localisation(df_gold_length, 2)
print(df_gold_length.head())
