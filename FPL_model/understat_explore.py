#%%
from understat import Understat

import aiohttp
import asyncio
import nest_asyncio
import json

import seaborn as sns
import pandas as pd

#%%
# this is required to allow nested run of asyncio i.e. to run it in a loop
nest_asyncio.apply()

#%%
# * * get all player names from the EPL from the different years
# think will download all the JSON data for all players

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        players = await understat.get_league_players(
            "epl",
            2018,
            team_title="Manchester United"
        )
        print(json.dumps(players))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


#%%
player_name = "aguero"
player = 619
fid_out = str(player_name) + ".json"
#%%

async def main():
    ''' get the data for all matches played by a player stored on understat'''
    
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        # Using **kwargs
        player_matches = await understat.get_player_matches(
            player)
        # output 
        with open(fid_out, 'w') as f:
            json.dump(player_matches, f)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#%%
fid_out = str(player_name) + ".json"
player_stats = pd.read_json(fid_out)
fid_out = str(player_name) + ".hdf"
player_stats.to_hdf(fid_out, '0')
# %%
