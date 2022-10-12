#%%
import seaborn as sns
import pandas as pd
import seaborn as sns
import yaml
import utils
import glob
import re
import unidecode
import json

#%%
home = "/Users/regesterdaniel/x_code/FPL_model"
path_out = home
#%%
params = utils.open_yaml(home, "params.yml")

#%%

player_paths_all = [path for path in glob.glob(home+"/Fantasy-Premier-League/data/**/players/*")]

player_folders_all = [player_paths_all[i].split('/')[-1] for i in range(len(player_paths_all))]

#remove accented characters and make lower case, replace all spaces and hypens with underscores
player_folders_stripped = utils.strip_player_names(player_folders_all)


#%%
player_folders_mapper = {player:[] for player in set(player_folders_stripped)}

for i, player in enumerate(player_folders_stripped):
    player_folders_mapper[player].append(player_paths_all[i])

#%%
fid = 'players_paths_FPLdata.json'
fid_out = os.path.join(home, fid)
json.dump(player_folders_mapper, open(fid_out, 'w' ), ensure_ascii=True, indent = 4)


# %%
