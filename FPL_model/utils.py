#%%
import seaborn as sns
import pandas as pd
import seaborn as sns
import os
import yaml


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
        yaml_file = yaml.safe_load(file_path)
        
    return yaml_file
# %%
