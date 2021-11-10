# Projet Python | Adam Gouja & Loïc Djinou

## Description du projet
### Analyse des matchs professionnels de League of Legends 

League of Legends est un jeu compétitif (MOBA) créé par Riot Games en 2009 qui se joue en équipe de 5. Deux équipes d'affrontent sur une carte et doivent détruire la base ennemie avant que l'équipe adverse ne le fasse. Les parties durent en général entre 20 et 45 minutes. Dans League of Legends existe un système de revenus (golds). Pour obtenir des golds, les joueurs ont plusieurs possibilités : tuer des unités ennemis, détruires des tourelles ou tuer les personnages des joueurs adverses. Avec ces revenus, les joueurs peuvent acheter des équipements qui leur permettront de combattre plus aisément. La différence de golds entre les équipes est la manière la plus facile de repérer si une équipe est en avance sur l'autre.
Voici une courte vidéo explicative de ce qu'est League of Legends :
https://www.youtube.com/watch?v=WD9qgO0jo-M&ab_channel=LeagueofLegends-France

Durant ce mini-projet nous allons analyser les matchs professionnels qui ont eu lieu entre 2014 et 2018 au Brésil, en Corée, en Europe, en Turquie et en Amérique du Nord.
L'objectif est de déterminer si il existe une réelle différence de niveau entre les équipes de ces pays. 


Pour effectuer ces analyses, nous avons utilisé les jeux de données suivants :
* [Kaggle](https://www.kaggle.com/chuckephron/leagueoflegends)

Nous avons aussi dû installer la bibliothèques suivante : pandas, numpy, geopy, plotly, dash, kaggle, os, shutil, folium et math

## User Guide

### Installation

* Pour récupérer notre projet, il faut saisir la commande suivante sur Git Bash : 

```
git clone https://github.com/AdamGouja/project-Python-for-DS
```
Il faut ensuite importer les bibliothèques qui sont regroupées dans le fichier requirements.txt. Pour cela, on utilise la commande :

```
pip install -r requirements.txt 
```

Afin de lancer le projet de la meilleure des manières, il faut avoir une clé kaggle que vous pouvez installer en suivant les consignes via le lien suivant :
https://www.kaggle.com/docs/api

Enfin, pour ouvrir le dashboard du projet, il suffit d'utiliser la commande suivante dans le terminal en se situant dans le répertoire du projet :
python main.py (pour Windows)
python3 main.py (pour Linux)
 

## Developer Guide

Le code est divisé en 2 fichiers : "get_data.py" et "main.py".

Le fichier "get_data.py" permet de récupérer les fichiers de données via le site web de kaggle. Les fichiers de données sont tout de même inclus dans le dossier data du projet.
Lors du téléchargement des données, la fonction va vérifier si le fichier .zip existe. Si c'est le cas nous ne téléchargeons pas les données, sinon nous les téléchargeons. 

Nous avons besoin pour l'instant dans notre projet de 2 fichiers issu de kaggle : "League of Legends.csv" et "golds.csv"

Le fichier "main.py" contient tout le traitement des données (ajout des données de localisation, modification de certaines valeurs, concaténation de tableaux etc.), la création du dashboard et son lancement.

### Le rapport

Notre dashboard affiche un histogramme, un graphique linéaire et deux cartes géographiques géolocalisées.

Tout d'abord, l'histogramme nous permet d'observer la longueur des matchs compétitifs présents dans chaque pays. Ceci peut nous donner une image du niveau des parties étant données que des parties avec de grandes différence de niveau vont avoir des longueurs très grandes ou très petites. On peut remarquer que dans notre cas, peu importe les pays et les années, la moyenne des parties se situent autour de 35-40 minutes. Le niveau à l'intérieur de chaque pays (donc de chaque ligue) est assez homogène.

Le graphique linéaire nous montre dans un second temps la moyenne de la différence de golds tout au long des parties. Nous avons choisi de caper nos données à la 40e minute afin d'avoir assez de données pour avoir des moyennes représentatives. Les données de ce graphique ont été récupérées via la concaténation de certaines informations du fichier 'LeagueofLegends.csv" et les informations contenues dans el fichier "golds.csv". Ce graphique a été créé de telle sorte que la différence de golds soit toujours en faveur de l'équipe qui gagne la partie. Nous pouvons alors voir l'évolution des parties et les analyser. La différence de golds est assez similaire selon les pays mais une chose saute aux yeux. on se rend compte que la différence de golds se fait très rapidement au cours des parties, ce qui signifie qu'il est assez rare de voir une équipe qui perd son avantage. Cependant plus la partie est longue et plus cet écart devient petit. On le remarque notamment par le fait qu'au bout d'un certain temps la courbe redescent. Ceci montre que les longues parties ont un écart au golds plus faible que celles qui durent moins longtemps.

Ces deux graphiques nous montrent donc que les parties selon les pays semblent assez similaire : une longueur moyenne des parties homogène, un écart au golds plus ou moins équivalent selon les pays. Cependant comment est-il possible de vérifier qu'un pays possède un niveau moyen plus élevé qu'un autre ?
Il existe dans League of Legends un coupe du monde que l'on appelle "Les Worlds". Les équipes les plus fortes de chaque région s'affrontent de manière classique à la manière d'un tournoi.
Une des manières donc de vérifier si une région a un niveau plus élevé que les autres est de regarder ses résultats dans cette compétition.

Grâce à nos deux cartes nous pouvons avoir une vision du niveau des régions dans la scène internationale entre 2014 et 2018. En effet, nous avons calculer le nombre d'apparitions aux Worlds de chaque pays. Etant donné que pour accéder aux Worlds, les équipes doivent passer par des phases qualificatives, seules les meilleures équipes au monde y accèdent. 
Notre première carte nous montre donc le nombre d'apparitions aux Worlds de chaque région. Plus le cercle est gros, plus la région a participé aux matchs. On peut voir que la Corée semble être la région où les équipes participent le plus aux Worlds. Nous pouvons donc avoir une idée de sa supprémacie au niveau de la scène internationale. L'Europe et L'Amérique du Nord semblent cependant avoir un niveau équivalent.

L'autre moyen de vérifier le niveau des régions est de comparer le nombre de victoires sur cette même scène internationale. C'est ce qui a été réalisé sur la deuxième carte du dashboard.
On remarque que le nombre de victoires suit la même logique que le nombre de matchs joués. Ceci nous confirme donc que la Corée incarne (du moins selon nos données) ce qui se fait le mieux en terme de niveau de jeu. Il est donc totalement possible qu'une équipe de bas de tableau de Corée soit en mesure de battre une équipe de haut de tableau de Turquie par exemple qui possède à son actif 4 matchs joués sur la scène internationale pour 0 victoires.

Un axe d'amélioration de ce projet serait d'effectuer des matchs "virtuels" entre les équipes en prenant en compte leur région, leur taux de victoire, leur différence de golds moyenne avec les équipes qu'elles affrontent etc. Ainsi nous pourrions potentiellement prédire l'issu de certains matchs et effectuer une simulation de compétition.

A partir de nos données nous pouvons donc établir un classement des régions :
1- Corée
2- Europe
3- Amérique du Nord
4- Brésil
5- Turquie