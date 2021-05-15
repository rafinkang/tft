import dbConn
import json

# 기물 정보
def load_champions_data() :
    insert_data_list = []
    json_data = get_json_data('champions')

    for champion in json_data :
        chp_info_list = [champion['championId'], champion['name'], int(champion['cost'])]

        for num in range(0, 3) : 
            if num <= len(champion['traits']) - 1 :
                chp_info_list.append(champion['traits'][num])
            else:
                chp_info_list.append(None)

        insert_data_list.append(chp_info_list)

    sql = "insert into champions_info(ci_chapion_id, ci_name, ci_cost, ci_traits_1, ci_traits_2, ci_traits_3) values(%s, %s, %s, %s, %s, %s);"

    load_data(sql, insert_data_list)

# 아이템 정보
def load_items_data() :
    insert_data_list = []
    json_data = get_json_data('items')

    for item in json_data :
        item_info_list = [item['id'], item['name'], 0 if item['isUnique'] else 1, 0 if item['isShadow'] else 1]
        insert_data_list.append(item_info_list)

    sql = "insert into items_info(ii_id, ii_name, ii_is_unique, ii_is_shadow) values(%s, %s, %s, %s);"

    load_data(sql, insert_data_list)

# 특성 정보
def load_traits_data() :
    insert_data_list = []
    json_data = get_json_data('traits')

    for trait in json_data :
        sets_dict = {'bronze_min' : None, 'bronze_max' : None, 'silver_min' : None, 'silver_max' : None, 'gold_min' : None, 'gold_max' : None, 'chromatic_min' : None}

        for sets in trait['sets'] : 
            style = sets['style']
            for key, value in sets.items() :
                if key != 'style' : 
                    sets_dict[style + '_' + key] = value

        trait_info_list = [trait['key'], trait['name'], trait['type'], sets_dict['bronze_min'], sets_dict['bronze_max'], sets_dict['silver_min'], sets_dict['silver_max'], sets_dict['gold_min'], sets_dict['gold_max'], sets_dict['chromatic_min']]

        insert_data_list.append(trait_info_list)

    sql = "insert into traits_info(ti_key, ti_name, ti_type, ti_bronze_min, ti_bronze_max, ti_silver_min, ti_silver_max, ti_gold_min, ti_gold_max, ti_chromatic_min) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    load_data(sql, insert_data_list)

# json 데이터 가져오기
def get_json_data(file_name) :
    json_data = None

    with open('C:\\Users\\jypar\\portfolio\\tft\\set5\\%s.json'%file_name, 'r', encoding='UTF8') as f:
        json_data = json.load(f)
    
    return json_data

# DB 저장
def load_data(sql, insert_data_list) :
    # DB에 저장되지 않게 print만 실행
    print(sql)
    print(insert_data_list)
    # db = dbConn.DbConn()
    # print(db.executemany(sql, insert_data_list))

# load_champions_data()
# load_items_data()
# load_traits_data()



