import datetime
import logging
import re

import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

file1 = open("token", "r")
file2 = open("channel", "r")


token = file1.read()
channel = file2.read()

last_value = 621.87

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_exchange():
    r = requests.get('http://si3.bcentral.cl/Indicadoressiete/secure/Indicadoresdiarios.aspx')
    soup = BeautifulSoup(r.text, 'html.parser')
    value = soup.find('table',{'id': 'tblDos'}).find('label', {'id': 'lblValor1_3'}).string
    return value

def force(bot, update):
    bot.send_message(chat_id = channel,
                     text = get_exchange())

def send_exchange(bot, job):
    global last_value
    a = get_exchange()
    msg = '💰 Valor del dólar en pesos chilenos: ' + a + '\n\n'
    a = a.replace(',', '.')
    dif = float(a) - last_value
    msg += 'Cambio con respecto al último valor: \n'
    if (dif > 0):
        msg += '↗ ' + "{:.2f}".format(dif) + ' (+' + "{:.4f}".format(dif/last_value) + ' %)'
    else:
        msg += '↘ ' + "{:.2f}".format(dif) + ' (' + "{:.4f}".format(dif/last_value) + ' %)'
    last_value = float(a)
    bot.send_message(chat_id=channel,
                     text=msg)

def main():
    updater = Updater(token)
    j = updater.job_queue
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("update123", force))
    j.run_daily(send_exchange, time=0)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    get_exchange()
