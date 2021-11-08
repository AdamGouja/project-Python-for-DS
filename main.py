#------------------------------------------------------------------------------IMPORTS------------------------------------------------------------------------------#

import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from get_data import get_data_LoL

#-----------------------------------------------------------------------------FUNCTIONS-----------------------------------------------------------------------------#

def new_df_length(df):
    """
    Crée un nouveau dataframe avec comme colonnes 'Address', 'League', 'Type', 'Year', 'blueTeamTag', 'bResult', 'rResult', 'redTeamTag' et 'gamelength'.

    Args:
        df : dataframe initial

    Returns:
        Nouveau dataframe.
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

#-----------------------------------------------------------------------------MAIN CODE-----------------------------------------------------------------------------#

get_data_LoL()

# Récupération de la data frame
initial_df = pd.read_csv("data/LeagueofLegends.csv")

# Création de la nouvelle dataframe avec les colonnes souhaitées
df_length = new_df_length(initial_df)

# ajout des colonnes permettant la localisation
add_localisation(df_length,2)

# Ajout des golds jusqu'à la minute 40
gold = pd.read_csv("data/gold.csv").query("Type=='golddiff'")
gold.drop(['Type'], axis=1, inplace=True)
gold.drop(gold.iloc[:,gold.columns.get_loc("min_41"):], axis=1, inplace=True)

df_gold_winside = pd.merge(df_length[['Address','rResult']], gold)
df_gold_winside.drop(["Address"], axis = 1, inplace=True)

i=0
for elements in df_gold_winside['rResult']:
    if elements == 1:   
        df_gold_winside.loc[i] = (-1)*df_gold_winside.loc[i]
    i+=1

df_gold_winside = pd.concat([gold['Address'], df_gold_winside], axis = 1)
df_gold_winside = pd.merge(df_length[['Address', 'Country','Year']], df_gold_winside)
df_gold_winside = df_gold_winside.drop(['rResult'], axis=1)

year = 2015
years1 = df_length['Year'].unique()
years2 = df_gold_winside['Year'].unique()


if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)

    hist_length = px.histogram(
        df_length[df_length['Year']==year], 
        x=['gamelength'],
        facet_col="Country", 
        color = "Country", 
        labels = {'value':'duration of the game (in minutes)'}
    )

    line_golds = px.line(
        df_gold_winside.query("Year=='"+str(year)+"'").groupby(['Country']).mean().T.drop(["Year"], axis = 0),
        color = 'Country'
    )

    app.layout = html.Div(children=[
                                    html.H1(
                                        id="title_project",
                                        children=f'Mini Project - Python for DataScience',
                                        style={'textAlign': 'center', 'color': '#03224C'} # (5)
                                    ),

                                    html.H3(
                                        id="names",
                                        children=f'Realised by Adam Gouja & Loïc Djinou',
                                        style={'textAlign': 'center', 'color': '#03224C'} # (5)
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
                                        style={'textAlign': 'center', 'color': '#6D071A'} # (5)
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
                                        style={'textAlign': 'center', 'color': '#6D071A'} # (5)
                                    ),

                                    html.Label(
                                        children = 'Year',
                                    ),

                                    dcc.Slider(
                                        id="year-slider2",
                                        min=min(years2),
                                        max=max(years2)-1,
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

                                ]
    )

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
                    df_gold_winside.query("Year=='"+str(input_value)+"'").groupby(['Country']).mean().T.drop(["Year"], axis = 0),
                    color = 'Country'
                ),

                f'Mean gold difference during the game for each country ({input_value})',

                f'''
                The graph above shows the mean gold difference at each minute for each Country in {input_value}.
                Mouse over for details.
                '''
                ]

    #-------------RUN APP-------------#
    app.run_server(debug=True)

    #                         

    #                         dcc.Interval(   id='interval',
    #                             interval=1*1000, # in milliseconds
    #                             n_intervals=0
    #                         ),

    #                          # (6)


    #                         html.Div(
    #                             id='description',

    #                             children=f'''

    #                             The graph above shows relationship between life expectancy and

    #                             GDP per capita for year {year}. Each continent data has its own

    #                             colour and symbol size is proportionnal to country population.

    #                             Mouse over for details.

    #                         '''), # (7)

    

    # ]

    # )


    # @app.callback(  Output('year-slider', 'value'),
    #                 [Input('interval', 'n_intervals')])
    # def on_tick(n_intervals):
    #     if n_intervals is None: return 0
    #     return years[(n_intervals+1)%len(years)]


    


     # (8)