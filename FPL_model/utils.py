#%%
import seaborn as sns
import pandas as pd
import seaborn as sns
import os
import yaml
import unidecode


def mkdir(home, out_folder):
    """function to make new directory using us.mkdir
    
    Args:
        home (_type_): home folder path
        out_folder (_type_): new folder to be made within the home folder
    """
    out_path = os.path.join(home, out_folder)
    if os.path.isdir(out_path) != True:
        os.mkdir(out_path)
        print("dir made: " + out_path)
    elif os.path.isdir(out_path) == True:
        print("dir already exists")
    else:
        print("error: dir not made")

    return



def open_yaml(path, fid):
    
    """opens yaml file using yaml.safe_load

    Returns:
        _type_: _description_
    """
    
    file_path = os.path.join(path, fid)
    
    with open(file_path) as file:
        yaml_file = yaml.safe_load(open(file_path))
        
    return yaml_file


def read_FPLdata_paths(paths_FPLdata):
    
    """FPLdata has separate folders for each season year, would like to read all year files at once for a single player
    this function will return a single concat df of all filepaths provided

    Returns:
        _type_: _description_
    """
    
    dfs = []
    for path in paths_FPLdata:
        dfs.append(pd.read_csv(path))

    player_FPLdata = pd.concat(dfs, axis = 0, ignore_index = True)
    
    return player_FPLdata
# %%
def strip_player_names(list_of_player_names):
    
    """strip player names of numbers, accented characters, capitals, spaces and hyphens

    Returns:
        _type_: _description_
    """
    player_folders_all_nonumbers=[]
    for player_folder in list_of_player_names:
        try:
            int(player_folder.split('_')[-1])
            player_folders_all_nonumbers.append('_'.join(player_folder.split('_')[0:-1]))
        except ValueError:
            player_folders_all_nonumbers.append(player_folder)
    
    list_of_player_names_stripped = [unidecode.unidecode(folder).lower().replace(' ',"_").replace('-', '_').replace("'", '') for folder in player_folders_all_nonumbers]
    
    return list_of_player_names_stripped