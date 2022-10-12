#%%
from black import out
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import seaborn as sns
import yaml
import utils
import os
import json
import glob
from tqdm import tqdm

#%%
home = "/Users/regesterdaniel/x_code/FPL_model/"
out_folder = "merged_player_data"
out_path = os.path.join(home, out_folder)

utils.mkdir(home, out_folder)

#%%
fid = 'params.yml'
params = utils.open_yaml(home, fid)

#%%
path_FPLdata = params["path_FPLdata"]
path_understat_data = params["path_understat"]
players = list(json.load(open('players_allyears.json')).keys())

#%%
# * logic for the algo is as follows:
# load all FPLdata for a given player and concat into single df
# set datetime as datetime and give key 'date'
# load understat_data and merge on 'date'
# ! ensure suitable way to deal with nan values

#%%
def read_FPLdata_paths(paths_FPLdata):
    dfs = []
    for path in paths_FPLdata:
        dfs.append(pd.read_csv(path))

    player_FPLdata = pd.concat(dfs, axis = 0, ignore_index = True)
    
    return player_FPLdata

#%%

player = players[0]

#%%
players_failed = []
for i in tqdm(range(len(players))):
    player = players[i]
    player_understat_fid = player + '.json'
    player_understat_path = os.path.join(path_understat_data, player_understat_fid)

    player_joined = '_'.join(player.split())
    player_split = player.split()
    
    try:
        paths_FPLdata = [path for path in glob.glob(path_FPLdata+"/**/**/*"+player_split[0]+"*"+player_split[1]+"*/gw.csv")]
        #process FPLdata
        player_FPLdata = read_FPLdata_paths(paths_FPLdata)
    except ValueError:
        try:
            #deal with case the surname and name are wrong way round
            paths_FPLdata = [path for path in glob.glob(path_FPLdata+"/**/**/*"+player_split[1]+"*"+player_split[0]+"*/gw.csv")]
            #process FPLdata
            player_FPLdata = read_FPLdata_paths(paths_FPLdata)
        except ValueError:
            #if above doesnt work then will ignore player as is typically those who have not played
            print('not doing player: ' + player)
            players_failed.append(player)
    except IndexError:
        try:
            #deal with case where there is only one name in understat data
            paths_FPLdata = [path for path in glob.glob(path_FPLdata+"/**/**/*"+player_split[0]+"*/gw.csv")]
            #process FPLdata    
            player_FPLdata = read_FPLdata_paths(paths_FPLdata)
        except ValueError:
            #if above doesnt work then will ignore player as is typically those who have not played
            print('not doing player: ' + player)
    

    _len = len(player_FPLdata['kickoff_time'])
    FPLdata_dates_for_merge = [player_FPLdata['kickoff_time'][i].split('T')[0] for i in range(_len)]

    player_FPLdata['date'] = FPLdata_dates_for_merge
    player_FPLdata['date'] =  pd.to_datetime(player_FPLdata['date'])

    #now process understat data
    player_understat_data = pd.DataFrame(json.load(open(player_understat_path)))
    player_understat_data['date'] =  pd.to_datetime(player_understat_data['date'])

    df_merge = pd.merge(player_understat_data, player_FPLdata, on = 'date', how ='outer')
    
    fid_out = os.path.join(out_path, player_joined+'.csv')
    df_merge.to_csv(fid_out)
    
#! next step = iterate over all players for the combined data and save
# * think the nan values from FPLdata in understat_data is when the player doesnt play
#%%




#%%
FPLdata_eg = "/Users/regesterdaniel/x_code/FPL_model/Fantasy-Premier-League/data/2020-21/players/Aaron_Ramsdale_483/gw.csv"
FPLdata = pd.read_csv(FPLdata_eg)
underset_data_path = "/Users/regesterdaniel/x_code/FPL_model/understat/pla_data/Aaron Ramsdale.json"
underset_data = pd.read_json(underset_data_path)

#%%
len_ = len(FPLdata['kickoff_time'])
FPLdata_dates_for_merge = [FPLdata['kickoff_time'][i].split('T')[0] for i in range(len_)]

FPLdata['date'] = FPLdata_dates_for_merge
FPLdata['date'] =  pd.to_datetime(FPLdata['date'])
                                    
#%%
df_merge = pd.merge(underset_data, FPLdata, on = 'date', how ='outer')

#%%
start_date = '2021-01-01'
end_date = '2021-12-30'
mask = (df_merge['date'] > start_date) & (df_merge['date'] <= end_date)
df2 = df_merge.loc[mask]

#%%

def get_player_data_understat(path_understat_data, player_name, year):
    
    
    
    