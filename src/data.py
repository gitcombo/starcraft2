import json
import datetime
import logging


logger = logging.getLogger('server_logger')
logger.info('*** Routing Data API ****')


def save(rank_list):
    save_db_data(rank_list)
    save_snapshot()
    save_last_snapshot(rank_list)
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def save_db_data(rank_list):
    logger.info('Saving sc2 data into database')
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    db = get_database()    
    db["last_checkpoint"] = today
    db[today] = get_daily_entry(rank_list)
    file = open(f"data/db.sci", "wt")
    file.write(json.dumps(db, indent=4))
    file.close()


def get_database():
    file = open("data/db.sci", "rt")
    db = json.loads(file.read())
    file.close()
    return db


def get_daily_entry(rank_list):
    logger.info('Getting daily entry')
    entry = {}        
    for player in json.loads(rank_list)['players']:
        entry[f"{player['name']}"]  = {
            "mmr" : player['mmr']
        }
    return entry


def save_snapshot():
    logger.info('Saving database snapshot')
    today = str(datetime.datetime.now().strftime("%Y-%m-%d"))    
    db = get_database()
    file = open(f"data/snapshots/db_{today}.sci", "wt")
    file.write(json.dumps(db, indent=4))
    file.close()


def save_last_snapshot(rank_list):
    logger.info('Saving last snapshot view data')
    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    rank = json.loads(rank_list)
    rank['last_checkpoint'] = today   
    file = open("data/snapshots/last_snapshot.sci", "wt")
    file.write(json.dumps(rank, indent=4))
    file.close()

