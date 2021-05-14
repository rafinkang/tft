import requests as req

# 게임 정보 가져오기
def get_match_info(params, user_name = None, summoner_id = None) :
    user_name = user_name
    user_info_url = 'https://kr.api.riotgames.com/tft/summoner/v1/summoners/'

    if user_name != None : user_info_url = user_info_url + 'by-name/' + user_name
    if summoner_id != None : user_info_url = user_info_url + summoner_id

    user_info_res = req.get(user_info_url, params = params)

    if user_info_res.status_code == 200 :
        user_info = user_info_res.json() # type of dict, 유저 정보
        user_puuid = user_info['puuid']

        match_url = 'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/%s/ids'%user_puuid
        params['count'] = 2
        match_res = req.get(match_url, params = params)

        if match_res.status_code == 200 :
            match_list = match_res.json() # type of dict, 경기 리스트, 최근부터 과거순으로 정렬되어 있음(아마도)

            for match in match_list : # 각 경기에 대한 상세 정보
                match_info_url = 'https://asia.api.riotgames.com/tft/match/v1/matches/' + match
                match_info_res = req.get(match_info_url, params = params)
                
                if match_info_res.status_code == 200 :
                    match_info = match_info_res.json()
                    print(match_info)
                    print('==============================================================================')


# 상위 티어 유저 정보 가져오기
def get_top_tier_info(params) :
    tier_dict = {'challenger' : [], 'grandmaster' : [], 'master' : []}
    tier_url = 'https://kr.api.riotgames.com/tft/league/v1/%s'

    for tier in tier_dict :
        res_tier = req.get(tier_url%tier, params = params)

        if res_tier.status_code == 200 :
            tier_dict[tier] = res_tier.json()['entries']
    
    return tier_dict


params = {'api_key' : 'RGAPI-1aedcf5c-6662-4861-85f0-db4176309fcc'} # api key
tier_dice = get_top_tier_info(params)

for tier_info in tier_dice['challenger'] : # tier_dice : 'challenger', 'grandmaster', 'master'
    summoner_name = tier_info['summonerName']
    summoner_id = tier_info['summonerId']

    print(summoner_name)
    get_match_info(params, summoner_id = summoner_id)



# get_match_info(params, user_name = '박빼뚤')

# get_match_info의 게임 정보
# {
#     "metadata": {
#         "data_version": "5",
#         "match_id": "KR_5188906277",
#         "participants": [유저들 puuid, ..........]
#     },
#     "info": {
#         "game_datetime": 1620724067851,
#         "game_length": 2132.9296875,
#         "game_version": "Version 11.9.372.2066 (Apr 23 2021/10:28:09) [PUBLIC] <releases 11.9="">",
#         "participants": [
#             {
#                 "companion": {
#                     "content_ID": "d6acad34-9974-4123-a91a-eb0853c07989",
#                     "skin_ID": 5,
#                     "species": "PetAkaliDragon"
#                 },
#                 "gold_left": 5,
#                 "last_round": 30,
#                 "level": 8,
#                 "placement": 6,
#                 "players_eliminated": 0,
#                 "puuid": "SUDMWoARtQDJpGPPlYRM7KtDVV0TvkHhUcxGa5cnQLhCSART16NBNeX3Mv0SP8RrU4LScmQ7v6XB6w",
#                 "time_eliminated": 1722.265625,
#                 "total_damage_to_players": 50,
#                 "traits": [
#                     {
#                         "name": "Set5_Cavalier",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 3
#                     },
#                     {
#                         "name": "Set5_Forgotten",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 3
#                     },
#                     {
#                         "name": "Set5_GodKing",
#                         "num_units": 1,
#                         "style": 3,
#                         "tier_current": 1,
#                         "tier_total": 1
#                     },
#                     {
#                         "name": "Set5_Hellion",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 3
#                     },
#                     {
#                         "name": "Set5_Ironclad",
#                         "num_units": 2,
#                         "style": 1,
#                         "tier_current": 1,
#                         "tier_total": 2
#                     },
#                     {
#                         "name": "Set5_Knight",
#                         "num_units": 5,
#                         "style": 2,
#                         "tier_current": 2,
#                         "tier_total": 3
#                     },
#                     {
#                         "name": "Set5_Legionnaire",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 4
#                     },
#                     {
#                         "name": "Set5_Nightbringer",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 4
#                     },
#                     {
#                         "name": "Set5_Ranger",
#                         "num_units": 1,
#                         "style": 0,
#                         "tier_current": 0,
#                         "tier_total": 2
#                     },
#                     {
#                         "name": "Set5_Redeemed",
#                         "num_units": 3,
#                         "style": 1,
#                         "tier_current": 1,
#                         "tier_total": 3
#                     },
#                     {
#                         "name": "Set5_Verdant",
#                         "num_units": 2,
#                         "style": 1,
#                         "tier_current": 1,
#                         "tier_total": 2
#                     }
#                 ],
#                 "units": [
#                     {
#                         "character_id": "TFT5_Poppy",
#                         "items": [],
#                         "name": "",
#                         "rarity": 0,
#                         "tier": 2
#                     },
#                     {
#                         "character_id": "TFT5_Varus",
#                         "items": [],
#                         "name": "",
#                         "rarity": 1,
#                         "tier": 1
#                     },
#                     {
#                         "character_id": "TFT5_Nautilus",
#                         "items": [],
#                         "name": "",
#                         "rarity": 1,
#                         "tier": 2
#                     },
#                     {
#                         "character_id": "TFT5_Thresh",
#                         "items": [],
#                         "name": "",
#                         "rarity": 1,
#                         "tier": 2
#                     },
#                     {
#                         "character_id": "TFT5_Taric",
#                         "items": [],
#                         "name": "",
#                         "rarity": 3,
#                         "tier": 1
#                     },
#                     {
#                         "character_id": "TFT5_Rell",
#                         "items": [
#                             1002,
#                             16
#                         ],
#                         "name": "",
#                         "rarity": 3,
#                         "tier": 1
#                     },
#                     {
#                         "character_id": "TFT5_Darius",
#                         "items": [
#                             57,
#                             19,
#                             37
#                         ],
#                         "name": "",
#                         "rarity": 4,
#                         "tier": 2
#                     },
#                     {
#                         "character_id": "TFT5_Kayle",
#                         "items": [
#                             15,
#                             23,
#                             1024
#                         ],
#                         "name": "",
#                         "rarity": 4,
#                         "tier": 1
#                     }
#                 ]
#             }, 
#               .........
#         ],
#         "queue_id": 1100,
#         "tft_game_type": "standard",
#         "tft_set_number": 5
#     }
# }

        

