import logging
import configparser
from src import battlenet, player, data, message


config = configparser.ConfigParser()
config.read('starcraft2.ini')
access_token = battlenet.get_access_token(config['battle.net']['client_id'], config['battle.net']['client_secret'])
logger = logging.getLogger('server_logger')
logger.info('*** Routing SC2 API ****')


def get_whatsapp_message():        
    player_list = player.load_players(access_token)
    rank_list = player.get_players_rank(player_list)
    return message.format_rank_message(rank_list, platform='whatsapp')


def save_daily_mmr():
    player_list = player.load_players(access_token)
    rank_list = player.get_players_rank(player_list)
    return data.save(rank_list)
