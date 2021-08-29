import json
import logging
import requests
import configparser
import time


config = configparser.ConfigParser()
config.read('starcraft2.ini')
logger = logging.getLogger('server_logger')
logger.info('*** Routing Player API ****')


def load_players(access_token):
    player_list = load_initial_player_data()
    player_list = complete_players_info(player_list, access_token)    
    return player_list


def load_initial_player_data():
    try:
        logger.info('Loading players...')
        player_file = open('data/players.sci', 'rt')
        player_list = json.loads(player_file.read())
        player_file.close()
    except FileNotFoundError:
        logger.critical('File not found: data/players.sci')
        raise FileNotFoundError('Players file not found')
    return player_list


def complete_players_info(player_list, access_token):
    players = player_list
    for player in players['players']:
        player = complete_player_info(player, access_token)    
    return players


def complete_player_info(player, access_token):
    logger.info('Player %s is loading ...', player['name'])    
    p = player
    p['mmr'] = get_player_mmr(player, access_token)       
    return p


def get_player_mmr(player, access_token):
    top_mmr = 0    
    ladder_list = get_player_ladders(player, access_token)    
    for ladder in ladder_list: 
        if '1v1' in ladder['localizedGameMode']:
            current_mmr = get_mmr(ladder['ladderId'], player, access_token)            
            if current_mmr > top_mmr: top_mmr = current_mmr
    return 0 if not ladder_list else top_mmr


def get_player_ladders(player, access_token):    
    try:        
        url = f"https://{player['region']}.api.blizzard.com/sc2/profile/{player['region_id']}/{player['realm_id']}/{player['profile_id']}/ladder/summary?locale=en_US&access_token={access_token}"
        logger.info('Getting ladder_list from: %s profile: %s', player['name'], player['profile_id'] )
        return get_response(url).json()['allLadderMemberships']
    except Exception as e:
        logger.critical(e)
        raise


def get_mmr(ladderId, player, access_token):
    try:        
        url = f"https://{player['region']}.api.blizzard.com/sc2/profile/{player['region_id']}/{player['realm_id']}/{player['profile_id']}/ladder/{ladderId}?locale=en_US&access_token={access_token}"
        mmr = get_response(url).json()['ranksAndPools'][0]['mmr']
        logger.info('mmr from: %s from ladder: %s is %s', player['name'], ladderId, str(mmr))
        return mmr
    except Exception as e:
        logger.critical(e)
        raise


def get_players_rank(player_list):   
    return rank_players(player_list)


def rank_players(player_list):
    rank_list = json.dumps({"players": sorted(player_list['players'], key=lambda k: k['mmr'], reverse=True)}, indent=4)    
    return rank_list


def get_response(url):
    try:
        response = requests.get(url)
        max_retry = config['app']['max_retry_count']
        retry_count = 0
        while response.status_code != 200 and retry_count < int(max_retry):
            time.sleep(1)
            response = requests.get(url)
            logger.info('response code: %s %s', response.status_code, response.text)
            retry_count += 1
        if (retry_count) >= int(max_retry): raise ConnectionError        
        if (response.status_code) == 401: raise Exception('Authentication failed. Check access token value.')
        return response
    except ConnectionError:
        logger.critical('Downstream error from battle-net.')
        raise

