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
out_folder = "pla_info"
out_path = os.path.join(home, out_folder)
if os.path.isdir(out_path) != True:
    os.mkdir(out_path)

#%%
# * * get all player names from the EPL from the different years
# think will download all the JSON data for all players

years = params['years']
player_ids= []
player_names = []
for year in years:

    async def main():
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            players = await understat.get_league_players(
                "epl",
                year,
            )
            print(len(players))
            for i in range(len(players)):
                #print(players[i]['player_name'] )
                player_names.append(str(players[i]['player_name']))
                player_ids.append(players[i]['id'])
            

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

player_info_understat = {player_names[i]: player_ids[i] for i in range(len(player_names))}
# output data
fid_out = os.path.join(out_path, "players_allyears" + ".json")
json.dump(player_info_understat, open(fid_out, 'w' ), ensure_ascii=True, indent = 4)


# %%


# %%
