from aiogram import Bot
from bs4 import BeautifulSoup
from asyncio import sleep
import requests, logging, traceback, datetime, re
from config import TOKEN_BOT
from updateDB import select_id, select_channel, ban_channel


logging.basicConfig(filename="log.out", level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')
bot = Bot(token=TOKEN_BOT)
current_date = datetime.datetime.now() - datetime.timedelta(hours=1, minutes=0)


months = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

async def parsing():
    while True:
        list_id_user = await select_id()
        for id_user in list_id_user:
            list_channel_from_user = await select_channel(id_user)
            for channel in list_channel_from_user:
                await answer(channel, id_user)
        global current_date
        current_date = datetime.datetime.now()
        await sleep(30)


async def answer(channel, id_user):
    try:
        response = requests.get(f"https://t.me/s/{channel[1:]}")
        soup = BeautifulSoup(response.text, 'lxml')
        
        #смотрим на ласт скрипт
        last_scripts = soup.find_all("script")[-1].text
        
        #если называется как TWeb.init(); - то канал, иначе парсим другой источник данных
        if last_scripts.strip() == "TWeb.init();":
            
            #берём название канала
            name_channel = soup.find("span").text
            
            #ищем все статьи
            all_articles = soup.find_all("div", class_="tgme_widget_message_wrap js-widget_message_wrap")
            
            #для каждой статьи получаем текст и время отправки
            all_articles = all_articles[::-1]
            for article in all_articles:
                #время поста
                time_article_str = article.find("time", class_="time").text
                time_article = datetime.datetime.strptime(time_article_str, "%H:%M") + datetime.timedelta(hours=3, minutes=0)
                #дата поста
                data_article_str = article.find("div", class_="tgme_widget_message_service_date_wrap")
                print(data_article_str)
                month = months[data_article_str.split()[0].lower()]
                day = data_article_str.split()[1]
                article_date = datetime.datetime(year=2023, month=int(month), day=int(day), hour=int(time_article.hour), minute=int(time_article.minute))
                print(f"Дата поста:{article_date}")
                #сравнимаем время и дату поста с текущим, если пост свежий, то парсим его
                if current_date < article_date:
                    #достаём текст
                    all_text = article.find("div", class_="tgme_widget_message_text js-message_text")
                    message = all_text.text
                    #отправляем сообщение
                    await bot.send_message(id_user, f"Сообщение из канала {name_channel} {channel}\n\n{message}\n\nОпубликовано в {str(time_article.time())[0:5]}")
                    await sleep(1)

        #если это не канал
        else:
            await bot.send_message(id_user, f"Возможно, канала {channel} не существует, или это не канал.\n\nКанал был помечен как не существующий и больше не будет отслеживаться")
            await ban_channel(channel)
    #если вышла ошибка
    except Exception as e:
        logging.error(f"{str(e)}")
        logging.error(str(traceback.format_exc()))
