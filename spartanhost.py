import telegram
import requests
import time


# 2$ per season
url1 = 'https://billing.spartanhost.net/cart.php?a=add&pid=245'
# 2.5$ per month 10G
url2 = 'https://billing.spartanhost.net/cart.php?a=add&pid=169'
bot = telegram.Bot(token='1412550215:AAE8cXKFaEPXTnsrXltWtA9tn0clF5grwl8')
while True:
    try:
        r1 = requests.get(url1)
        r2 = requests.get(url2)
        res1 = r1.status_code
        res2 = r2.status_code
        if res1 == 200:
            if 'Out of Stock' not in r1.text:
                message = 'Important! spartanhost 2$/season is on sale!'
                bot.send_message(chat_id='@Hermes_messager', text=message)
            else:
                pass
        else:
            pass
        if res2 == 200:
            if 'Out of Stock' not in r2.text:
                message = ' Spartanhost 2.5$/m 10G bandwidth is on sale!'
                bot.send_message(chat_id='@Hermes_messager', text=message)
            else:
                pass
        else:
            pass
    except:
        pass
    time.sleep(3600)