import logging
from dotenv import load_dotenv
import tweepy
import os
from logging import handlers



class Configurator:
    load_dotenv()
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO,
                        filename = "logs/logfile.log", filemode = "w")
    handler = handlers.TimedRotatingFileHandler("logs/logfile.log", when='midnight')
    handler.setFormatter(logging.Formatter(log_format, datefmt="%d-%m-%Y %H:%M:%S"))
    logging.info(f'Starting up..')

    @staticmethod
    def create_clients():
        con_key = os.environ.get('CON_KEY')
        con_secret = os.environ.get('CON_SECRET')
        acc_secret = os.environ.get('ACC_SECRET')
        acc_key = os.environ.get('ACC_KEY')
        bearer = os.environ.get('BEARER_TOKEN')

        auth = tweepy.OAuthHandler(con_key, con_secret)
        auth.set_access_token(acc_key, acc_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3, retry_delay=3)
        client = tweepy.Client(consumer_key=con_key, consumer_secret=con_secret,
                               access_token=acc_key, access_token_secret=acc_secret, bearer_token=bearer,
                               wait_on_rate_limit=True)
        try:
            api.verify_credentials()
        except Exception as e:
            logging.error("Error creating api", exc_info=True)
            raise e
        logging.info("api and Client created")
        return api, client
