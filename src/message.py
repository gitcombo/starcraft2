import json
import logging
from datetime import datetime


logger = logging.getLogger('server_logger')
logger.info('*** Routing Message API ****')


def format_rank_message(player_list, platform):
    logger.info('formatting message for %s', platform)
    if (platform == 'whatsapp'): return format_whatsapp(player_list)


def format_whatsapp(player_list):
    message = header(player_list, 'whatsapp') + body(player_list, 'whatsapp') + footer('whatsapp')
    logger.info('message: \n%s', message)
    return message


def header(player_list, platform): 
    if platform == 'whatsapp': return header_whatsapp()


def body(player_list, platform): 
    if platform == 'whatsapp': return body_whatsapp(player_list)


def footer(platform): 
    if platform == 'whatsapp': return footer_whatsapp()


def header_whatsapp():
    header = "------------------------------------\n"
    header = header + "\t<Wasa> Rank\n"
    header = header + "------------------------------------\n"    
    return header


def body_whatsapp(player_list):
    i = 0    
    body = ""
    players = json.loads(player_list)['players']
    top_mmr = players[0]['mmr']
    for player in players:
        i += 1
        delta_mmr = top_mmr - player['mmr']
        body = body + "{:0>2d}. {} *{:0>4d}* mmr ({}{:0>4d})"\
            .format(i, player['name'][0:6], player['mmr'], \
                get_sign(delta_mmr), abs(delta_mmr)) + "\n"        
        top_mmr = player['mmr']
    return body


def get_sign(x):
    return '+' if (x >= 0) else '-'


def footer_whatsapp():    
    footer = "------------------------------------"
    footer += f"\nTime           : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer += f"\nLast Checkpoint: {get_last_snapshot()['last_checkpoint']}"
    footer += "\n------------------------------------"
    return footer


def get_last_snapshot():
    try:
        file = open("data/snapshots/last_snapshot.sci", "rt")
        last_snapshot = json.loads(file.read())
        file.close()
        return last_snapshot
    except FileNotFoundError:
        return {"players":[], "last_checkpoint": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}


def get_delta_mmr(player):    
    for p in get_last_snapshot()['players']: 
        if p['name'] == player['name']:
            return player['mmr'] - p['mmr']
    return 0

