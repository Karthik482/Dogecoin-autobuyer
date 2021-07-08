import logging
import traceback
import tweepy
import re
import robin_stocks.robinhood as rs
from time import sleep
from datetime import datetime
import logging


# save logs(time and date)

current_time = datetime.now().strftime("%Y%m%d-%H_%M_%S")
st = r"C:\RMLogs\log\ {0}.txt".format(current_time)
LOG_FORMAT = "%(levelname)s %(asctime)s -%(message)s"

logging.basicConfig(filename=st,
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='w')

logger = logging.getLogger()

# ENTER TWITTER API KEY'S FROM TWITTER DEV WEBSITE

consumer_key = "ENTER CONSUMER_KEY"
consumer_secret = 'ENTER CONSUMER SECRET'
key = "ENTER KEY"
secret = "ENTER SECRET KEY"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


def login_robin(your_username, your_password):
    rs.login(username=your_username,
             password=your_password,
             expiresIn=86400,
             by_sms=True)


def buy_doge(symbol, quantity):
    rs.orders.order_buy_crypto_by_quantity(symbol,
                                           quantity,
                                           timeInForce='gtc')
    # sell doge after 100 seconds
    sleep(100)

    rs.orders.order_sell_crypto_by_quantity(symbol,
                                            quantity,
                                            timeInForce="gtc")


def main():
    login_robin("Enter robinhood username", "Enter robinhood password")
    while True:
        elon_tweets = api.user_timeline("elonmusk")
        for tweet in elon_tweets[:1]:
            try:
                # tweet comes in utc time zone
                twt_time = tweet.created_at
                txt_conv = tweet.text
                # getting current utc time
                now = datetime.utcnow()
                # difference in seconds between current local time and tweet time
                diff_sec = ((now - twt_time).total_seconds())
                # buy only if tweet was posted less than 1 second
                if diff_sec < 1:
                    #search if tweet as "dog" character  mentioned in his tweet
                    TorF = bool(re.search("dog", txt_conv, re.IGNORECASE))
                    if TorF:
                        #if mentioned buy 1 coin of Doge
                        buy_doge("DOGE", 1)
                    else:
                        print("No mention of doge in this tweet")
                else:
                    print("last tweet was posted more than a second ago")
            except:
                logger.error(traceback.print_exc())


if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        print('Press any key to continue...')
