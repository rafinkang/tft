import dbConn
import json

def load_champions_data():
    db = dbConn.DbConn()
    json_data = None
    insert_data_list = []

    with open('C:\\Users\\jypar\\portfolio\\tft\\set5\\champions.json', 'r') as f:
        json_data = json.load(f)

    for champion in json_data :
        chp_info_list = [champion['championId'], champion['name'], int(champion['cost'])]

        for num in range(0, 3) : 
            if num <= len(champion['traits']) - 1 :
                chp_info_list.append(champion['traits'][num])
            else:
                chp_info_list.append(None)

        insert_data_list.append(chp_info_list)

    sql = "insert into champions_info(ci_chapion_id, ci_name, ci_cost, ci_traits_1, ci_traits_2, ci_traits_3) values(%s, %s, %s, %s, %s, %s);"
    print(db.executemany(sql, insert_data_list))

# load_champions_data()
