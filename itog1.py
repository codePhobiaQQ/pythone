import requests
import ast
import telebot

BOT_TOKEN = '1913814505:AAH4wAx4ENSd1MEQ6vTlvOxeLettqG1R1tE'
URL_KUNA = 'https://api.kuna.io/v3/book/usdtrub'
URL_GARAN = 'https://garantex.io/api/v2/coinmarketcap/orderbook/USDT_RUB'
def get_data_kuna(URL_USDTRUB):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r = requests.get(URL_USDTRUB, headers=HEADERS)
    market = r.text
    mark = ast.literal_eval(market)
    course_asks_1 = []
    volume_asks_1 = []
    course_bids_1 = []
    volume_bids_1 = []
    total_volume_asks = 0
    total_volume_bids = 0

    for st in mark: 
        if st[1] < 0:
            course_asks_1.append(st[0])
            volume_asks_1.append(-st[1])
        else:
            course_bids_1.append(st[0])
            volume_bids_1.append(st[1])

    i = 0
    sr1 = 0
    while total_volume_asks + volume_asks_1[i] <= 20000 and i < len(volume_asks_1):
        total_volume_asks += volume_asks_1[i]
        sr1 += volume_asks_1[i] * course_asks_1[i]
        i += 1 
    sr1 += ((20000 - total_volume_asks)*course_asks_1[i])
    sr1 = (sr1*0.9975)/20000

    j = 0
    sr2 = 0
    while total_volume_bids + volume_bids_1[j] <= 20000 and j < len(volume_bids_1):
        total_volume_bids += volume_bids_1[j]
        sr2 += volume_bids_1[j] * course_bids_1[j]
        j += 1
    sr2 += ((20000 - total_volume_bids)*course_bids_1[j])
    sr2 = (sr2*0.9975)/20000
    return [sr1, sr2]

def get_data_garantex(URL_USDTRUB):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r = requests.get(URL_USDTRUB, headers=HEADERS)
    market = r.text
    mark = ast.literal_eval(market)
    course_asks_2 = []
    volume_asks_2 = []
    course_bids_2 = []
    volume_bids_2 = []
    total_volume_asks = 0
    total_volume_bids = 0

    for st in mark['asks']:
        course_asks_2.append(float(st[0]))
        volume_asks_2.append(float(st[1]))

    for st1 in mark['bids']:
        course_bids_2.append(float(st1[0]))
        volume_bids_2.append(float(st1[1]))

    i = 0
    sr1 = 0
    while total_volume_asks + volume_asks_2[i] <= 20000 and i < len(volume_asks_2):
        total_volume_asks += volume_asks_2[i]
        sr1 += volume_asks_2[i] * course_asks_2[i]
        i += 1 
    sr1 += ((20000 - total_volume_asks)*course_asks_2[i+1])
    sr1 = (sr1*0.998)/20000

    j = 0
    sr2 = 0
    while total_volume_bids + volume_bids_2[j] <= 20000 and j < len(volume_bids_2):
        total_volume_bids += volume_bids_2[j]
        sr2 += volume_bids_2[j] * course_bids_2[j]
        j += 1
    sr2 += ((20000 - total_volume_bids)*course_bids_2[j])
    sr2 = (sr2*0.998)/20000
    return [sr1, sr2]

def get_data_bitzlato():
    pass

def resalt(x, y):
    price = x + y
    g_k = {'Разница между ASK на Kuna и ASK на Gar': '', 'Разница между ASK на Kuna и BID на Gar': '', 'Разница между BID на Kuna и ASK на Gar': '', 'Разница между BID на Kuna и BID на Gar': '',}
    a_a = 100*abs(price[0] - price[2])/min(price[0], price[2])
    g_k['Разница между ASK на Kuna и ASK на Gar'] = a_a
    a_b = 100*abs(price[0] - price[3])/min(price[0], price[3])
    g_k['Разница между ASK на Kuna и BID на Gar'] = a_b
    b_a = 100*abs(price[1] - price[2])/min(price[1], price[2])
    g_k['Разница между BID на Kuna и ASK на Gar'] = b_a
    b_b = 100*abs(price[1] - price[3])/min(price[1], price[3])
    g_k['Разница между BID на Kuna и BID на Gar'] = b_b
    return g_k


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend!")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower():
            try:
                bot.send_message(
                    message.chat.id,
                    f'{resalt(get_data_kuna(URL_KUNA), get_data_garantex(URL_GARAN))}'
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )

    bot.polling(none_stop=True, timeout=123)


if __name__ == '__main__':
    # get_data()
    telegram_bot(BOT_TOKEN)

#pip install PyTelegramBotAPI==3.6.7
