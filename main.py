import pandas as pd
import geopy
from geopy.geocoders import Nominatim

#-----------------------------------------------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def new_df_gold_length(df):
    """
    Crée un nouveau dataframe avec comme colonnes 'League', 'Type', 'blueTeamTag', 'bResult', 'rResult', 'redTeamTag', 'gamelength' et 'golddiff'.

    Args:
        df : dataframe initial

    Returns:
        Nouveau dataframe.
    """
    df2 = df[['League', 'Type','blueTeamTag','bResult','rResult','redTeamTag','gamelength','golddiff']]

    df2=df2[(df2['League'] == 'NALCS') | 
            (df2['League'] == 'LCK')   | 
            (df2['League'] == 'EULCS') |
            (df2['League'] == 'TCL')   |
            (df2['League'] == 'CBLoL') ]
            
    df2= df2[(df2['Type'] != 'Regional') & 
             (df2['Type'] != 'Promotion')]

    return df2

def add_localisation(df, position):
    """
    Ajoute une colonne "Country", "Lattitude" et "Longitude" au dataframe mis en argument selon la ligue du match en question.

    Args:
        df : dataframe où ajouter les colonnes
        position : numéro de la colonne à partir de laquelle ajouter les colonnes
    """
    
    # NALCS : Amérique du Nord
    # LCK : Corée
    # EULCS : Europe
    # LMS : Taiwan Hong-Kong Macao
    # TCL : Turquie
    # OPL : Océanie
    # WC : World Cup
    # CBLoL : Brésil

    app = Nominatim(user_agent="Adam")

    loc_k  = app.geocode("Korea").raw
    loc_na = app.geocode("North America").raw
    loc_eu = app.geocode("Europe").raw
    loc_br = app.geocode("Brazil").raw
    loc_t  = app.geocode("Turkey").raw

    k  = [loc_k["lat"] , loc_k["lon"]]
    na = [loc_na["lat"], loc_na["lon"]]
    eu = [loc_eu["lat"], loc_eu["lon"]]
    br = [loc_br["lat"], loc_br["lon"]]
    t  = [loc_t["lat"] , loc_t["lon"]]

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
    df["Lattitude"] = df["Lattitude"].astype("float")
    df["Longitude"] = df["Longitude"].astype("float")

def gold_to_list(df):
    """
    Modifie la colonne "golddiff" en passant ses valeurs de string à list.

    Args:
        df : dataframe où mettre la colonne
    """
    new_gold_diff = []

    for elements in df["golddiff"]:
        i=1
        s=''
        tab=[]
        num = 0
        for i in range (1,len(elements)):
            if elements[i] == ',' or elements[i] == ']':
                num = pd.to_numeric(s)
                s='' 
                tab.append(num)   
            else :
                s=s+elements[i]            
            i=i+1
        new_gold_diff.append(tab)

    position = df.columns.get_loc("golddiff")
    del df["golddiff"]
    df.insert(position, "golddiff", new_gold_diff)


#-----------------------------------------------------------------------------MAIN CODE-----------------------------------------------------------------------------#

#Récupération de la data frame
df = pd.read_csv("data/LeagueofLegends.csv")

#Création de la nouvelle dataframe avec les colonnes souhaitées
df_gold_length = new_df_gold_length(df)

#ajout des colonnes permettant la localisation
add_localisation(df_gold_length,1)

#modification de la colonne des golds, passage de string à list
gold_to_list(df_gold_length)
print(df_gold_length.head())
