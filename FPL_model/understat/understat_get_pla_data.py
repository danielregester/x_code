#%%
from understat import Understat

import aiohttp
import asyncio
import nest_asyncio
import json
import os

import seaborn as sns
import pandas as pd
import yaml


#%%
# this is required to allow nested run of asyncio i.e. to run it in a loop
nest_asyncio.apply()
#%%
with open('params.yml') as file:
  params= yaml.safe_load(file)
#%%

home = "/Users/regesterdaniel/x_code/FPL_model/understat"
out_folder = "pla_data"
out_path = os.path.join(home, out_folder)
if os.path.isdir(out_path) != True:
    os.mkdir(out_path)
    

#%%
years = params['years']
#%%
player_info = json.load(open(os.path.join(home, "pla_info", "players_allyears.json")))

#%%
# * get all data for players in player_list - obtained by ubderstat_get_pla_info.py

for player, id in player_info.items():
    player_data = []
    async def main():
        ''' get the data for all matches played by a player stored on understat'''
        
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            # Using **kwargs
            player_matches = await understat.get_player_matches(
                id)
            # output 
            print(len(player_matches))
            
            for i in range(len(player_matches)):
                player_data.append(player_matches[i])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
    fid_out = os.path.join(out_path, player + ".json")
    json.dump(player_data, open(fid_out, 'w' ), ensure_ascii=True, indent = 4)



# %%
