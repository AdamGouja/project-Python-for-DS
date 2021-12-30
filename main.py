#------------------------------------------------------------------------------IMPORTS------------------------------------------------------------------------------#

from numpy.core.numeric import NaN
import pandas as pd
# import geopy
from geopy.geocoders import Nominatim
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from get_data import get_data_LoL
import folium
import math


#-----------------------------------------------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def new_df_length(df):
    """
    Crée un nouveau dataframe avec comme colonnes 'Address', 'League', 'Type', 'Year', 'blueTeamTag', 'bResult', 'rResult', 'redTeamTag' et 'gamelength'.

    Args:
        df (dataframe) : dataframe initial

    Returns:
        (dataframe) : Nouveau dataframe.
    """
    df2 = df[['Address', 'League', 'Type', 'Year', 'blueTeamTag', 'bResult', 'rResult', 'redTeamTag', 'gamelength']]

    df2=df2[(df2['League'] == 'NALCS') | 
            (df2['League'] == 'LCK')   | 
            (df2['League'] == 'EULCS') |
            (df2['League'] == 'TCL')   |
            (df2['League'] == 'CBLoL') ]
            
    df2= df2[(df2['Type'] != 'Regional') & 
             (df2['Type'] != 'Promotion')]

    return df2

def get_localisation():
    """
    Récupère la lattitude et la longitude des pays suivants : Corée, Amérique du Nord, Europe, Brésil et Turquie. 

    Returns:
        k (list): Lattitude et Longitude de la Corée.
        na (list): Lattitude et Longitude de l'Amérique du Nord.
        eu (list): Lattitude et Longitude de l'Europe.
        br (list): Lattitude et Longitude du Brésil.
        t (list): Lattitude et Longitude de la Turquie.
    """
    app = Nominatim(user_agent="Adam")

    loc_k  = app.geocode("Korea").raw
    loc_na = app.geocode("North America").raw
    loc_eu = app.geocode("Europe").raw
    loc_br = app.geocode("Brazil").raw
    loc_t  = app.geocode("Turkey").raw

    k  = [float(loc_k["lat"]) , float(loc_k["lon"])]
    na = [float(loc_na["lat"]), float(loc_na["lon"])]
    eu = [float(loc_eu["lat"]), float(loc_eu["lon"])]
    br = [float(loc_br["lat"]), float(loc_br["lon"])]
    t  = [float(loc_t["lat"]), float(loc_t["lon"])]

    return k,na,eu,br,t

def teams_loc_apparition_wins(df, initial_df):
    """
    Ajoute une colonne Country, Lattitude et Longitude pour chacune des équipes du dataframe mis en paramètre.

    Args:
        df (dataframe): dataframe où ajouter les colonnes.

    Returns:
        apparitions (list): liste contenant le nombre d'apparition des équipes d'Amérique du Nord, de Corée, d'Europe, de Turquie et du Brésil.
        wins (list): liste contenant le nombre de victoires des équipes d'Amérique du Nord, de Corée, d'Europe, de Turquie et du Brésil.
    """
    bCountry = []
    bLattitude = []
    bLongitude = []
    rCountry = []
    rLattitude = []
    rLongitude = []

    # Nombre d'apparitions de chaque pays
    NA_app = 0
    K_app = 0
    EU_app = 0
    TU_app = 0
    BR_app = 0

    # Nombre de victoires de chaque pays
    NA_win = 0
    K_win = 0
    EU_win = 0
    TU_win = 0
    BR_win = 0

    k,na,eu,br,t = get_localisation()
    df_teams = initial_df[['League', 'blueTeamTag','bResult','rResult','redTeamTag']]
    NA_Teams = League_teams(df_teams, 'NALCS')
    K_Teams = League_teams(df_teams, 'LCK')
    EU_Teams = League_teams(df_teams, 'EULCS')
    TU_Teams = League_teams(df_teams, 'TCL')
    BR_Teams = League_teams(df_teams, 'CBLoL')

    for i in range(len(df)):
        if df['blueTeamTag'].iloc[i] in NA_Teams:
            bCountry.append('North America')
            bLattitude.append(na[0])
            bLongitude.append(na[1])
            if df['bResult'].iloc[i] == 1:
                NA_win+=1
            NA_app+=1
        elif df['blueTeamTag'].iloc[i] in EU_Teams:
            bCountry.append('Europe')
            bLattitude.append(eu[0])
            bLongitude.append(eu[1])
            if df['bResult'].iloc[i] == 1:
                EU_win+=1
            EU_app+=1
        elif df['blueTeamTag'].iloc[i] in K_Teams:
            bCountry.append('Korea')
            bLattitude.append(k[0])
            bLongitude.append(k[1])
            if df['bResult'].iloc[i] == 1:
                K_win+=1
            K_app+=1
        elif df['blueTeamTag'].iloc[i] in TU_Teams:
            bCountry.append('Turkey')
            bLattitude.append(t[0])
            bLongitude.append(t[1])
            if df['bResult'].iloc[i] == 1:
                TU_win+=1
            TU_app+=1
        elif df['blueTeamTag'].iloc[i] in BR_Teams:
            bCountry.append('Brazil')
            bLattitude.append(br[0])
            bLongitude.append(br[1])
            if df['bResult'].iloc[i] == 1:
                BR_win+=1
            BR_app+=1
        else:
            bCountry.append(None)
            bLattitude.append(None)
            bLongitude.append(None)
        if df['redTeamTag'].iloc[i] in NA_Teams:
            rCountry.append('North America')
            rLattitude.append(na[0])
            rLongitude.append(na[1])
            if df['rResult'].iloc[i] == 1:
                NA_win+=1
            NA_app+=1
        elif df['redTeamTag'].iloc[i] in EU_Teams:
            rCountry.append('Europe')
            rLattitude.append(eu[0])
            rLongitude.append(eu[1])
            if df['rResult'].iloc[i] == 1:
                EU_win+=1
            EU_app+=1
        elif df['redTeamTag'].iloc[i] in K_Teams:
            rCountry.append('Korea')
            rLattitude.append(k[0])
            rLongitude.append(k[1])
            if df['rResult'].iloc[i] == 1:
                K_win+=1
            K_app+=1
        elif df['redTeamTag'].iloc[i] in TU_Teams:
            rCountry.append('Turkey')
            rLattitude.append(t[0])
            rLongitude.append(t[1])
            if df['rResult'].iloc[i] == 1:
                TU_win+=1
            TU_app+=1
        elif df['redTeamTag'].iloc[i] in BR_Teams:
            rCountry.append('Brazil')
            rLattitude.append(br[0])
            rLongitude.append(br[1])
            if df['rResult'].iloc[i] == 1:
                BR_win+=1
            BR_app+=1
        else:
            rCountry.append(None)
            rLattitude.append(None)
            rLongitude.append(None)
    
    df.insert(df.columns.get_loc("blueTeamTag")-1, "bCountry", bCountry)
    df.insert(df.columns.get_loc("blueTeamTag")-1, "bLattitude", bLattitude)
    df.insert(df.columns.get_loc("blueTeamTag")-1, "bLongitude", bLongitude)
    df.insert(df.columns.get_loc("redTeamTag")+1, "rLongitude", rLongitude)
    df.insert(df.columns.get_loc("redTeamTag")+1, "rLattitude", rLattitude)
    df.insert(df.columns.get_loc("redTeamTag")+1, "rCountry", rCountry)

    apparitions = [NA_app,TU_app,EU_app,K_app,BR_app]
    wins = [NA_win,TU_win,EU_win,K_win,BR_win]

    return apparitions, wins

def add_localisation(df, position):
    """
    Ajoute une colonne "Country", "Lattitude" et "Longitude" au dataframe mis en argument selon la ligue du match en question.

    Args:
        df (dataframe): dataframe où ajouter les colonnes.
        position (int): numéro de la colonne à partir de laquelle ajouter les colonnes.
    """
    
    # NALCS : Amérique du Nord
    # LCK : Corée
    # EULCS : Europe
    # LMS : Taiwan Hong-Kong Macao
    # TCL : Turquie
    # OPL : Océanie
    # WC : World Cup
    # CBLoL : Brésil

    k, na, eu, br, t = get_localisation()

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

def League_teams(df_teams, League:str):
    """
    Crée un tableau avec le nom des équipes qui ont participé à au moins un match compétitif dans la Ligue en paramètre.

    Args:
        df_teams (dataframe): dataframe contenant tous les matchs de toutes les Leagues.
        League (str): Nom de la Ligue d'où on veut récupérer les équipes qui la compose.

    Returns:
        (list): Tableau des équipes composant la Ligue mise en paramètre
    """
    df = df_teams[(df_teams['League']==League)]
    League_Teams = []
    for i in range(len(df)):
        if df['blueTeamTag'].iloc[i] not in League_Teams:
            League_Teams.append(df['blueTeamTag'].iloc[i])
        if df['redTeamTag'].iloc[i] not in League_Teams:
            League_Teams.append(df['redTeamTag'].iloc[i])
    return League_Teams

def new_df_gold(df, df_length):
    """
    Crée un dataframe avec la différence de golds selon l'équipe qui a gagné la partie

    Args:
        df (dataframe): dataframe des golds.
        df_length (dataframe): dataframe contenant les résultats des parties.

    Returns:
        (dataframe) : Nouveau dataframe.
    """
    gold = df.query("Type=='golddiff'")
    gold.drop(['Type'], axis=1, inplace=True)
    gold.drop(gold.iloc[:,gold.columns.get_loc("min_41"):], axis=1, inplace=True)
    df_gold_winside = pd.merge(df_length[['Address','rResult']], gold)
    df_gold_winside_with_addresses = df_gold_winside.copy()
    df_gold_winside.drop(["Address"], axis = 1, inplace=True)

    i=0
    for elements in df_gold_winside['rResult']:
        if elements == 1:   
            df_gold_winside.loc[i] = (-1)*df_gold_winside.loc[i]
        i+=1

    df_gold_winside = pd.concat([df_gold_winside_with_addresses['Address'], df_gold_winside], axis = 1)
    df_gold_winside = pd.merge(df_length[['Address', 'Country','Year']], df_gold_winside)
    df_gold_winside = df_gold_winside.drop(['rResult'], axis=1)

    return df_gold_winside
    
def filterNoneType(lis):
    """
    Supprime les données manquantes de la chaîne de caractère mise en paramètre.

    Args:
        lis (list): liste sous forme de chaîne de caractère

    Returns:
        (list): liste sous forme de chaîne de caractère avec les données vide supprimées
    """
    lis2 = []
    for l in lis: #filter out NoneType
        if type(l) == str:
            lis2.append(l)
    return lis2

def map(df_wc, show, str_show:str):
    """
    Génère une carte qui sera enregistrée dans le répertoire local.

    Args:
        df_wc (dataframe): dataframe utilisée pour la création de la carte
        show (list): données à afficher
        str_show (str): nom de la donnée à afficher
    """
    countries = filterNoneType(list(df_wc['bCountry'].unique()))
    lats = [x for x in df_wc['bLattitude'].unique() if math.isnan(x) == False]
    longs = [x for x in df_wc['bLongitude'].unique() if math.isnan(x) == False]
    games = show
    coords = (48.8398094,2.5840685)

    # Création de la map
    map = folium.Map(location=coords, zoom_start=2)
    for i in range(len(countries)):
        folium.CircleMarker(
            location = (lats[i], longs[i]),
            radius = games[i]/2,
            color = 'crimson',
            fill = True,
            fill_color = 'crimson',
            tooltip = 'Number of '+str_show+' : '+str(games[i])+
                    "\n"+'Country : '+countries[i]
        ).add_to(map)
    map.save(outfile = str_show+'.html')

#-----------------------------------------------------------------------------MAIN CODE-----------------------------------------------------------------------------#

#Récupération des données à partir d'internet
get_data_LoL()

# Récupération de la data frame
initial_df = pd.read_csv("data/LeagueofLegends.csv")

initial_df

# Création de la dataframe avec les colonnes souhaitées pour la longueur des parties
df_length = new_df_length(initial_df)

# Ajout des colonnes permettant la localisation
add_localisation(df_length,df_length.columns.get_loc("League")+1)

# Création de la dataframe des golds jusqu'à la minute 40
gold = pd.read_csv("data/gold.csv")
df_gold_winside = new_df_gold(gold, df_length)

# Initialisation des équipes de chaque Ligue
df_teams = initial_df[['League', 'blueTeamTag','bResult','rResult','redTeamTag']]
NA_Teams = League_teams(df_teams, 'NALCS')
K_Teams = League_teams(df_teams, 'LCK')
EU_Teams = League_teams(df_teams, 'EULCS')
TU_Teams = League_teams(df_teams, 'TCL')
BR_Teams = League_teams(df_teams, 'CBLoL')

# Création du dataframe pour les matchs internationaux
df_wc = initial_df[['Address', 'League', 'Year', 'blueTeamTag','bResult','rResult','redTeamTag','gamelength']]
df_wc = df_wc[(initial_df['League']=='WC')]

# Ajout des localisations et création des variables du nombre de parties de chaque pays
apparition, win = teams_loc_apparition_wins(df_wc, initial_df)

# Création des cartes
map(df_wc,apparition,'apparitions')
map(df_wc,win,'wins')

# Création des variables
year = 2015
years1 = df_length['Year'].unique()
years2 = df_gold_winside['Year'].unique()


if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    #-------------GRAPHS-------------#
    hist_length = px.histogram(
        df_length[df_length['Year']==year], 
        x=['gamelength'],
        facet_col="Country", 
        color = "Country", 
        labels = {'value':'duration of the game (in minutes)'}
    )

    line_golds = px.line(
        df_gold_winside[df_gold_winside['Year'] == year].groupby(['Country']).mean().T.drop(["Year"]),
        color = 'Country'
    )

    

    #-------------LAYOUT-------------#
    app.layout = html.Div(children=[
                                    html.H1(
                                        id="title_project",
                                        children=f'Mini Project - Python for DataScience',
                                        style={'textAlign': 'center', 'color': '#03224C'}
                                    ),

                                    html.H3(
                                        id="names",
                                        children=f'Realised by Adam Gouja & Loïc Djinou',
                                        style={'textAlign': 'center', 'color': '#03224C'}
                                    ),

                                    html.Div(
                                        id='description_LoL',
                                        children=f'''
                                        League of Lengends is a competitive 5vs5 game created by Riot Games in 2009. The objective of the game is to destroy the enemy base.
                                        The games least between 20 and 45 minutes in general.
                                        Here we will analyze the professional games between 2015 and 2018 in Brazil, Korea, Western Europe, Turkey and North America.
                                        '''
                                    ),

                                    html.Div(
                                        id='description_objective',
                                        children=f'''
                                        The objective of this project is to find if there is a real difference between the games of every Country since they are all playing 
                                        the same game.
                                        '''
                                    ),
                                
                                    html.H2(
                                        id="title_gamelength",
                                        children=f'Duration of games depending on the Country ({year})',
                                        style={'textAlign': 'center', 'color': '#6D071A'}
                                    ),

                                    html.Label(
                                        children = 'Year',
                                    ),

                                    dcc.Slider(
                                        id="year-slider",
                                        min=min(years1),
                                        max=max(years1),
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        value=year,
                                    ),

                                    dcc.Graph(
                                        id='graph_gamelength',
                                        figure=hist_length
                                    ),

                                    html.Div(
                                        id='description_graph_gamelength',
                                        children=f'''
                                        The graph above shows the number of games that ended at each minute for year {year}.
                                        Each country data has its own colour and graph.
                                        Mouse over for details.
                                        '''
                                    ),

                                    html.H2(
                                        id="title_golddiff",
                                        children=f'Mean gold difference during the game for each country ({year})',
                                        style={'textAlign': 'center', 'color': '#6D071A'}
                                    ),

                                    html.Label(
                                        children = 'Year',
                                    ),

                                    dcc.Slider(
                                        id="year-slider2",
                                        min=min(years2),
                                        max=max(years2),
                                        tooltip={"placement": "bottom", "always_visible": True},
                                        value=year,
                                    ),

                                    dcc.Graph(
                                        id='graph_golddiff',
                                        figure=line_golds
                                    ),

                                    html.Div(
                                        id='description_graph_golddiff',
                                        children=f'''
                                        The graph above shows the mean gold difference at each minute for each Country in {year}.
                                        Mouse over for details.
                                        '''
                                    ),

                                    html.H2(
                                        id="title_map_apparition",
                                        children=f'Number of apparitions in World Cups for every Country',
                                        style={'textAlign': 'center', 'color': '#6D071A'}
                                    ),
                                    
                                    html.Iframe(
                                        id = 'map_apparition',
                                        srcDoc = open('apparitions.html', 'r').read(),
                                        width= '70%',
                                        height= 600,
                                    ),

                                    html.Div(
                                        id='description_map_apparition',
                                        children=f'''
                                        The map above shows the number of games played in World Cups for each Country between 2014 and 2018.
                                        Mouse over for details.
                                        '''
                                    ),

                                    html.H2(
                                        id="title_map_wins",
                                        children=f'Number of wins in World Cups for every Country',
                                        style={'textAlign': 'center', 'color': '#6D071A'}
                                    ),

                                    html.Iframe(
                                        id = 'map_wins',
                                        srcDoc = open('wins.html', 'r').read(),
                                        width= '70%',
                                        height= 600,
                                        title= 'Number of wins in World Cup for each Country' 
                                    ),

                                    html.Div(
                                        id='description_map_win',
                                        children=f'''
                                        The map above shows the number of games won in World Cups for each Country between 2014 and 2018.
                                        Mouse over for details.
                                        '''
                                    ),

                                ]
    )

    #-------------CALLBACKS-------------#
    @app.callback(
        [Output(component_id='graph_gamelength', component_property='figure'), 
         Output(component_id='title_gamelength', component_property='children'),
         Output(component_id='description_graph_gamelength', component_property='children')],
        [Input(component_id='year-slider', component_property='value')],
    )
    def update_figure(input_value): 
        return [px.histogram(df_length[df_length['Year']==input_value], 
                            x=['gamelength'],
                            facet_col="Country", 
                            color = "Country", 
                            labels = {'value':'duration of the game (in minutes)'}),

                f'Duration of games depending on the Country ({input_value})',

                f'''
                The graph above shows the number of games that ended at each minute for year {input_value}.
                Each country data has its own colour and graph.
                Mouse over for details.
                '''
                ]


    @app.callback(
        [Output(component_id='graph_golddiff', component_property='figure'), 
         Output(component_id='title_golddiff', component_property='children'),
         Output(component_id='description_graph_golddiff', component_property='children')],
        [Input(component_id='year-slider2', component_property='value')],
    )
    def update_figure2(input_value): 
        return [px.line(
                    df_gold_winside[df_gold_winside['Year'] == input_value].groupby(['Country']).mean().T.drop(["Year"]),
                    color = 'Country'
                ),

                f'Mean gold difference during the game for each country ({input_value})',

                f'''
                The graph above shows the mean gold difference at each minute for each Country in {input_value}.
                Mouse over for details.
                '''
                ]

    #-------------RUN APP-------------#
    app.run_server()
    