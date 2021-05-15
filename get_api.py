import requests as req
import dbConn
from time import sleep

# 상위 티어 유저 정보 가져오기
def get_top_tier_info(params) :
    # tier_dict = {'challenger' : [], 'grandmaster' : [], 'master' : []}
    tier_list = ['challenger', 'grandmaster', 'master']
    tier_url = 'https://kr.api.riotgames.com/tft/league/v1/%s'
    res_list = []

    for tier in tier_list :
        res_tier = req.get(tier_url%tier, params = params)

        if res_tier.status_code == 200 :
            tier_summ_list = res_tier.json()['entries']
            insert_data_list = []
    
            for tier_info in tier_summ_list : # 각 티어별 소환사 정보
                insert_data_list.append([tier_info['summonerId'], tier_info['summonerName'], tier_info['leaguePoints'], tier])

            db = dbConn.DbConn()
            sql = "insert into summoner(s_id, s_name, s_points, s_tier) values(%s, %s, %s, %s) on duplicate key update s_name = values(s_name), s_points = values(s_points), s_tier = values(s_tier);"
            res = db.executemany(sql, insert_data_list)
            res_list.append(res)
    
    return res_list

# 사용자 puuid 가져오기
def get_puuid(params, user_name = None, summoner_id = None) :
    user_name = user_name
    user_info_url = 'https://kr.api.riotgames.com/tft/summoner/v1/summoners/'
    user_puuid = None

    if user_name != None : user_info_url = user_info_url + 'by-name/' + user_name
    if summoner_id != None : user_info_url = user_info_url + summoner_id

    user_info_res = req.get(user_info_url, params = params)

    if user_info_res.status_code == 200 :
        user_info = user_info_res.json() # type of dict, 유저 정보
        user_puuid = user_info['puuid']
    
    return user_puuid

# 매치 리스트 가져오기
def get_match_list(params, summoner_puuid, count = 20) :
    match_url = 'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/%s/ids'%summoner_puuid
    params['count'] = count # 몇 경기 가져올 것인가
    match_res = req.get(match_url, params = params)
    match_list = []

    if match_res.status_code == 200 :
        match_list = match_res.json() # type of dict, 경기 리스트, 최근부터 과거순으로 정렬되어 있음(아마도)

    return match_list

# 각 매치에 대한 상세 정보
def get_match_info(params, match_list) : 
    for match in match_list :
        match_info_url = 'https://asia.api.riotgames.com/tft/match/v1/matches/' + match
        match_info_res = req.get(match_info_url, params = params)
        
        if match_info_res.status_code == 200 :
            match_info = match_info_res.json()
            print(match_info)
            print('==============================================================================')




# 서머너 테이블 가져와서 s_puuid 없는 애들 채워 넣기 
def insert_puuid(params) :
    db = dbConn.DbConn()
    sql = "SELECT * FROM summoner WHERE s_puuid IS null"
    puuid_is_null = db.selectdict(sql)
    
    for i in puuid_is_null:
        puuid = get_puuid(params, summoner_id=i['s_id'])
        sql = f"UPDATE summoner SET s_puuid = '{puuid}' WHERE s_no={i['s_no']}"
        db.execute(sql)
        sleep(1)
    
# 매치 리스트 채워넣기
def insert_match_list(params) :
    db = dbConn.DbConn()
    match_list = []
    
    # puuid 리스트 만들어서 
    sql = "SELECT s_puuid FROM summoner where s_puuid IS not null"
    puuid_list = db.selectdict(sql)
    # puuid_list = db.select(sql)
    # print(type(puuid_list), puuid_list)
    
    # get_match_list 를 통해 api 호출
    i = 1
    j = len(puuid_list)
    for pl in puuid_list:
        puuid = pl['s_puuid']
        get_match = get_match_list(params, puuid, count = 30)
        # match_list.append(get_match)
        match_list.extend(get_match)
        
        print(i, '/', j, '-----진행중 !!')
        i += 1
        sleep(1)
    
    # 중복을 제거 한 후 
    print('전체 리스트:', len(match_list))
    match_list = list(set(match_list))
    print('중복 제거 리스트:', len(match_list))
    
    # 인서트
    sql = "insert into match_list(ml_match) values(%s) on duplicate key update timestamp = CURRENT_TIMESTAMP();"
    res = db.executemany(sql, match_list)
    print('db insert:', res)


# 실행단
if __name__ == "__main__":

    params = {'api_key' : 'RGAPI-91c42e63-0451-47a0-ae44-b4f32bb18174'} # api key

    # 1. 티어 dictionary 가져오기
    # print(get_top_tier_info(params)) 
    
    # 2. 서머너 테이블 가져와서 s_puuid 없는 애들 채워 넣기 
    # insert_puuid(params) 

    # 3. 매치 리스트 채워 넣기 (중복제거해서 넣어야 해)
    insert_match_list(params)






# for tier_info in tier_dict['challenger'] : # tier_dict : 'challenger', 'grandmaster', 'master'
#     summoner_name = tier_info['summonerName']
#     summoner_id = tier_info['summonerId']

#     summoner_puuid = get_puuid(params, summoner_id = summoner_id) # 사용자 puuid 가져오기
#     match_list = get_match_list(params, summoner_puuid) # 사용자가 참여한 매치 리스트 가져오기 (default = 20개)
#     get_match_info(params, match_list) # 각 매치에 대한 상세정보 조회




# get_match_info(params, user_name = '박빼뚤')

# get_match_info의 게임 정보
# {
#     "metadata": {
#         "data_version": "5",
#         "match_id": "KR_5188906277",
#         "participants": [유저들 puuid, ..........]
#     },
#     "info": {
#         "game_datetime": 1620724067851, # unix timestamp
#         "game_length": 2132.9296875, # 초단위 게임 길이
#         "game_version": "Version 11.9.372.2066 (Apr 23 2021/10:28:09) [PUBLIC] <releases 11.9="">",
#         "participants": [
#             {
#                 "companion": {
#                     "content_ID": "d6acad34-9974-4123-a91a-eb0853c07989",
#                     "skin_ID": 5,
#                     "species": "PetAkaliDragon"
#                 },
#                 "gold_left": 5, # 게임 끝난 후 남은 골드
#                 "last_round": 30, # 라운드 수
#                 "level": 8, # 레벨
#                 "placement": 6, # 순위
#                 "players_eliminated": 0, # 제거한 플레이어 수
#                 "puuid": "SUDMWoARtQDJpGPPlYRM7KtDVV0TvkHhUcxGa5cnQLhCSART16NBNeX3Mv0SP8RrU4LScmQ7v6XB6w",
#                 "time_eliminated": 1722.265625, # 참가자가 제거되기 까지 걸리 초
#                 "total_damage_to_players": 50, # 다른 참가자에게 준 피해량
#                 "traits": [
#                     {
#                         "name": "Set5_Cavalier", # 시너지 종류
#                         "num_units": 1, # 해당 시너지 기물 수
#                         "style": 0, # tier_current의 style
#                         "tier_current": 0, # 해당 시너지의 현재 단계
#                         "tier_total": 3 # 해당 시너지의 총 단계가 몇개 있나
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
#                         "character_id": "TFT5_Poppy", # 기물 아이디(이름 포함)
#                         "items": [], # 기물이 착용중인 아이템
#                         "name": "", # 종종 비워둔데(항상인듯)
#                         "rarity": 0, # 코스트 - 1 값
#                         "tier": 2 # 몇 성인가
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

        

