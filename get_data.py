import os
import kaggle
import shutil

def get_data_LoL():
    """
    Importe les fichiers de données dans un dossier data du répertoire de travail.
    """
    kaggle.api.authenticate()

    if("leagueoflegends.zip" not in os.listdir()):
        kaggle.api.dataset_download_files("chuckephron/leagueoflegends")
    else : print("files already downloaded")

    shutil.unpack_archive("leagueoflegends.zip", "./data")