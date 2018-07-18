# encoding:UTF-8
# python3.6
import requests
import json
import time, threading

difficulty_dict = ['low', 'mid', 'high']
score_dict = ['595', '1190', '2380']

def get_planets():
    r = requests.get('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanets/v0001/',
                     params={"active_only": "1", "language": "schinese"})
    planets = r.json()['response']['planets']
    return planets

def print_planets(planets):
    for planet in planets:
        planet_id = planet['id']
        name = planet['state']['name']
        progress = planet['state']['capture_progress']
        difficulty = planet['state']['difficulty']
        print('星球id：{}  星球名：{}  进度：{} difficulty:{} '.format(planet_id, name, progress, difficulty))

def select_planets(planets):
    idlist = []
    for planet in planets:
        planet_id = planet['id']
        idlist.append(planet_id)
        name = planet['state']['name']
        progress = planet['state']['capture_progress']
        print('星球id：{}  星球名：{}  进度：{}'.format(planet_id, name, progress))
    flag = 0
    while(flag == 0):
        select_id = input('请输入要进行游戏的星球的数字id：')
        try:
            if select_id in idlist:
                print('已成功选择')
                flag = 1
            else:
                print('输入错误，请确定输入的id可用')
        except Exception as e:
            print('Error:', e)
    return select_id


def autoselect_planets(planets):
    progress = 0.0
    for planet in planets:
        if planet['state']['capture_progress'] < 1:
            if planet['state']['capture_progress'] > progress:
                progress = planet['state']['capture_progress']
                select_id = planet['id']
                name = planet['state']['name']
            else:
                pass
        else:
            pass
    print('星球id：{}  星球名：{}  进度：{}'.format(select_id, name, progress))
    return select_id


def joinplanet(access_token, planet_id):
    requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/JoinPlanet/v0001/',
                  params={'id': planet_id, 'access_token': access_token})


def leaveplanet(access_token, planet_id):
    requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/LeaveGame/v0001/',
                  params={'gameid': planet_id, 'access_token': access_token})

def for_group(access_token):
    requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/RepresentClan/v0001/',
                  params={'clanid': '103582791429777370', 'access_token': access_token})

def autoselect_zone(planet_id, difficulty_limit=1):
    r = requests.get('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanet/v0001/',
                     params={'id': '{}'.format(planet_id), "language": "schinese"})
    data = r.json()['response']['planets'][0]
    name = data['state']['name']
    zones = data['zones']
    zones.reverse()
    position = {}
    position['2'] = []
    position['1'] = []
    for zone in zones:
        if zone['captured'] == False:
            difficulty = zone['difficulty']
            if difficulty == 3:
                select_zone = zone['zone_position']
                break
            elif difficulty >= difficulty_limit:
                position[str(difficulty)].append(zone['zone_position'])
    if difficulty == 3:
        pass
    else:
        if position['2'] != []:
            select_zone = position['2'][0]
            difficulty = 2
        elif position['1'] != []:
            select_zone = position['1'][0]
            difficulty = 1
        else:
            select_zone = None
            difficulty = None
    return [name, select_zone, difficulty]


def select_zone(planet_id, select_zone):
    r = requests.get('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanet/v0001/',
                     params={'id': '{}'.format(planet_id), "language": "schinese"})
    data = r.json()['response']['planets'][0]
    name = data['state']['name']
    zones = data['zones']
    for zone in zones:
        if zone['zone_position'] == int(select_zone):
            if zone['captured'] == False:
                difficulty = zone['difficulty']
                return [name, select_zone, difficulty]
            else:
                print('该位置已经被占领，请重新选择')
                return [name, None]
            break
        else:
            pass
    else:
        print('未找到该位置，请重新选择')
        return [name, None]


def leavezone(access_token, select_zone):
    requests.post('https://community.steam-api.com/IMiniGameService/LeaveGame/v0001/',
                  params={'gameid': select_zone, 'access_token': access_token})


def get_playerinfo(access_token):
    r = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlayerInfo/v0001/',
                      data={'access_token': access_token})
    data = r.json()['response']
    return data


def play(access_token, zone_position, difficulty):

    r = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/JoinZone/v0001/',
                      data={'zone_position': str(zone_position), 'access_token': access_token, })
    print(r.status_code)
    try:
        progress = r.json()['response']['zone_info']['capture_progress']
        print('已成功加入，等待120s发送分数')
        post_data = {'access_token': access_token,
                     'score': score_dict[difficulty-1], "language": "schinese"}
        time.sleep(120)
        
        for x in range(1,4):
            r = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/ReportScore/v0001/', data=post_data)
            result = r.json()['response']
            if result.__contains__('new_score'):
                print('分数发送成功，目前经验值：{}'.format(result['new_score']))
                return [True, result]
            else:
                print('分数发送失败 time: ' + str(x))

        return [False, 1]        
    except Exception as e:
        print('Error:', e)
        return [False, 0]

def run_game(user, access_token):    
    planets = get_planets()
    #difficulty_limit = int(input('3 高难度；2 中等难度；1 低难度（即所有难度均加入）\n请输入加入房间的最低难度（输入纯数字）：'))
    difficulty_limit = 1
    planets_function = autoselect_planets
    zone_function = autoselect_zone
   
    playerinfo = get_playerinfo(access_token)
    print('level:{} score:{}/{}\n'.format(playerinfo['level'],
                                          playerinfo['score'], playerinfo['next_level_score']))
    if playerinfo.__contains__('active_zone_game'):
        leavezone(access_token, playerinfo['active_zone_game'])
    if playerinfo.__contains__('active_planet'):
        leaveplanet(access_token, playerinfo['active_planet'])
    planet_id = planets_function(planets)
    joinplanet(access_token, planet_id)

    pause = 0
    while(pause == 0):
        print('\n'+time.asctime(time.localtime(time.time())))
        playerinfo = get_playerinfo(access_token)
        print('user:{} level:{} score:{}/{}\n'.format(user, playerinfo['level'],
                                              playerinfo['score'], playerinfo['next_level_score']))

        zone_data = autoselect_zone(planet_id, difficulty_limit)
        print(zone_data)
        if zone_data[1] != None:
            zone_position = zone_data[1]
            difficulty = zone_data[2]
            print('星球：{}\n已选择房间 {}，难度为：{}，预计获得的分数:{}'.format(
                zone_data[0], zone_position, difficulty_dict[difficulty-1], score_dict[difficulty-1]))
            info = play(access_token, zone_position, difficulty)
            if info[0] == False and info[1] == 0:
                pause = 0
            else:
                pass
        else:
            if planets_function == autoselect_planets:
                print('{}没有可以进行游戏的房间了，重新选择星球'.format(zone_data[0]))
                leaveplanet(access_token, planet_id)
                planets = get_planets()
                planet_id = planets_function(planets)
                joinplanet(access_token, planet_id)
            else:
                pass

if __name__ == '__main__':    
    access_token_bottle = '6a3a6b2ba0539aeef96ae814f223eabe'
    access_token_walker = '0b1d29e1e9118ccb121a105dc3a60f19'
    t1 = threading.Thread(target=run_game, args=('bottle', access_token_bottle)).start()
    t2 = threading.Thread(target=run_game, args=('walker', access_token_walker)).start()
