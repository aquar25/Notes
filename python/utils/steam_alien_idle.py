# encoding:UTF-8
# python3.6
import requests
import json
import time, threading

BASE_URL = 'https://community.steam-api.com/ITerritoryControlMinigameService'
BASE_URL_LEAVE = 'https://community.steam-api.com/IMiniGameService'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36',
             'Referer':'https://steamcommunity.com/saliengame/play/',
             'Origin': 'https://steamcommunity.com',
             'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
             }
ERROR_KEY = 'X-error_message'

difficulty_dict = ['low', 'mid', 'high']
score_dict = ['595', '1190', '2380']

def get_planets():
    r = requests.get(BASE_URL + '/GetPlanets/v0001/',
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
    progress = 1.0
    for planet in planets:
        if planet['state']['capture_progress'] < 1:
            if planet['state']['capture_progress'] <= progress:
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
    resp = requests.post(BASE_URL + '/JoinPlanet/v0001/',
                  data={'id': planet_id, 'access_token': access_token},
                  headers=headers)
    if ERROR_KEY in resp.headers:
        err_msg = str(resp.headers[ERROR_KEY])
        print(err_msg)
        leaveNum = err_msg.split(' ')[-1]
        if leaveNum == planet_id:
            pass
        else:
            leaveplanet(access_token, leaveNum)
            time.sleep(10)
            joinplanet(access_token, planet_id)

    print('join planet status', resp.status_code)

def leaveplanet(access_token, planet_id):
    resp = requests.post(BASE_URL_LEAVE+'/LeaveGame/v0001/',
                  data={'gameid': planet_id, 'access_token': access_token},
                  headers=headers)
    print('leave planet:{} status:{}'.format(planet_id, resp.status_code))


def for_group(access_token):
    requests.post(BASE_URL+'/RepresentClan/v0001/',
                  data={'clanid': '103582791429777370', 'access_token': access_token},
                  headers=headers)

def autoselect_zone(planet_id, difficulty_limit=1):
    r = requests.get(BASE_URL+'/GetPlanet/v0001/',
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
    r = requests.get(BASE_URL+'/GetPlanet/v0001/',
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
    resp = requests.post(BASE_URL_LEAVE+'/LeaveGame/v0001/',
                  params={'gameid': select_zone, 'access_token': access_token})
    print('leave zone:{} status:{}'.format(select_zone, resp.status_code))


def get_playerinfo(access_token):
    r = requests.post(BASE_URL+'/GetPlayerInfo/v0001/',
                      data={'access_token': access_token})
    data = r.json()['response']
    return data

def join_zone(user_config, zone_position):
    resp = requests.post(BASE_URL + '/JoinZone/v0001/',
                      data={'zone_position': str(zone_position), 'access_token': user_config['token']},
                      headers=headers)
    if ERROR_KEY in resp.headers:
        err_msg = str(resp.headers[ERROR_KEY])
        print(err_msg)
        leaveNum = err_msg.split(' ')[-1]
        if leaveNum == zone_position:
            print(user_config['user'] + 'already in zone')
            return 1
        else:
            leavezone(user_config['token'], leaveNum)
            time.sleep(10)
            join_zone(user_config['token'], zone_position)
    elif len(resp.json()['response']) == 0:
        print(user_config['user'] + "join zone no response right now...")
        return 0
    else:
        print(user_config['user'] + 'zone progress' + str(resp.json()['response']['zone_info']['capture_progress']))
        return 1


def play(user_config, zone_position, difficulty):
    code = join_zone(user_config, zone_position)
    if code == 0:
        return [False, 0]
    try:
        print(user_config['user'] + ' 已成功加入，等待120s发送分数')
        post_data = {'access_token': user_config['token'],
                     'score': score_dict[difficulty-1], "language": "schinese"}
        time.sleep(120)

        for x in range(1,5):
            r = requests.post(BASE_URL+'/ReportScore/v0001/', data=post_data, headers=headers)
            result = r.json()['response']
            if result.__contains__('new_score'):
                print('user:{} 分数发送成功，目前经验值：{}'.format(user_config['user'], result['new_score']))
                return [True, result]
            else:
                print('user:{} 分数发送失败 time:{}'.format(user_config['user'], str(x)) )
                time.sleep(1)

        return [False, 1]
    except Exception as e:
        print('Error:', e)
        return [False, 0]

def run_game(user, token):
    user_config = {'user':user, 'token':token}
    planets = get_planets()    
    difficulty_limit = 1
    planets_function = autoselect_planets

    playerinfo = get_playerinfo(user_config['token'])
    print('level:{} score:{}/{}\n'.format(playerinfo['level'],
                                          playerinfo['score'], playerinfo['next_level_score']))

    if playerinfo.__contains__('active_zone_game'):
        print('player active_zone_game {} '.format(playerinfo['active_zone_game']))
        leavezone(user_config['token'], playerinfo['active_zone_game'])

    if playerinfo.__contains__('active_planet'):
        print('player active_planet {} '.format(playerinfo['active_planet']))
        leaveplanet(user_config['token'], playerinfo['active_planet'])

    planet_id = planets_function(planets)
    joinplanet(user_config['token'], planet_id)

    pause = 0
    while(pause == 0):
        print('\n'+time.asctime(time.localtime(time.time())))
        playerinfo = get_playerinfo(user_config['token'])
        print('user:{} level:{} score:{}/{}\n'.format(user_config['user'], playerinfo['level'],
                                              playerinfo['score'], playerinfo['next_level_score']))

        zone_data = autoselect_zone(planet_id, difficulty_limit)
        if zone_data[1] != None:
            zone_position = zone_data[1]
            difficulty = zone_data[2]
            print('星球：{}\n已选择房间 {}，难度为：{}，预计获得的分数:{}'.format(
                zone_data[0], zone_position, difficulty_dict[difficulty-1], score_dict[difficulty-1]))
            info = play(user_config, zone_position, difficulty)
            if info[0] == False and info[1] == 0:
                pause = 0
            else:
                pass
        else:
            if planets_function == autoselect_planets:
                print('{}没有可以进行游戏的房间了，重新选择星球'.format(zone_data[0]))
                leaveplanet(user_config['token'], planet_id)
                planets = get_planets()
                planet_id = planets_function(planets)
                joinplanet(user_config['token'], planet_id)
            else:
                pass

if __name__ == '__main__':    
    t1 = threading.Thread(target=run_game, args=('bottle', '')).start()
    time.sleep(60)
    t2 = threading.Thread(target=run_game, args=('walker', '')).start()
