import logging
import requests


logger = logging.getLogger('server_logger')
logger.info('*** Routing Data API ****')


def get_access_token(client_id, client_secret):    
    try: 
        url = f"https://us.battle.net/oauth/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
        response = requests.post(url)
        logger.info('Getting access token status code: %s [%s]', str(response.status_code), response.text)        
        return response.json()['access_token']
    except KeyError:        
        raise KeyError("Please, check or update client id and client secret to get an access token.")

