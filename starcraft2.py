import logging
from src import log, wasa
from flask import Flask


app = Flask(__name__)
log.set_logger()
logger = logging.getLogger('server_logger')
error_message = {
            "Response": "Colud not retrieve information right now. Please, try again in a while.",
            "status_code": 500
        }


@app.route('/')
def _get_welcome_screen():    
    return "<h1>Welcome, <b>WASA v2.0</b> players.</h1>"


@app.route('/api/wasa/whatsapp')
def _get_whatsapp_rank_message():
    try:
        return wasa.get_whatsapp_message()
    except Exception as e:
        logger.critical(f"/api/wasa/whatsapp critical issue: {str(e)}")
        return error_message


@app.route('/api/db/daily_save')
def _save_daily_mmr():
    try:
        return wasa.save_daily_mmr()
    except Exception as e:
        logger.critical(f"/api/wasa/whatsapp critical issue: {str(e)}")
        return error_message


if __name__ == "__main__":
    app.run(host='0.0.0.0')
