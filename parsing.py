from aiogram import Bot
from bs4 import BeautifulSoup
from asyncio import sleep
import requests, asyncio, logging, traceback, datetime
from config import TOKEN_BOT
from updateDB import select_id, select_channel, ban_channel


logging.basicConfig(filename="log.out", level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s')
bot = Bot(token=TOKEN_BOT)
time_current = datetime.time(22, 55, 00)


async def main():
    while True:
        list_id_user = await select_id()
        for id_user in list_id_user:
            list_channel_from_user = await select_channel(id_user)
            for channel in list_channel_from_user:
                await answer(channel, id_user)
        global time_current
        time_current = datetime.datetime.now().time()
        print(f"Текущее время: {time_current}")
        await sleep(20)


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
                time_article = datetime.datetime.strptime(time_article_str, "%H:%M")
                #добавляем 3 часа ко времени публикации
                delta = datetime.timedelta(hours=3, minutes=0)
                time = (time_article + delta).time()
                #сравнимаем время поста и текущее, если пост свежий, то парсим его
                if time_current<time:
                    #достаём фото и видео
                    all_photo_and_video = article.find("div", class_="tgme_widget_message_grouped_layer js-message_grouped_layer")
                    
                    #достаём фото
                    if all_photo_and_video!=None:
                        all_photo = all_photo_and_video.find_all('a', class_="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo")
                    
                    #достаём видео
                    if all_photo_and_video!=None:
                        all_photo = all_photo_and_video.find_all('a', class_="tgme_widget_message_photo_wrap grouped_media_wrap blured js-message_photo")
                        
                    #достаём текст
                    message = ""
                    all_text = article.find("div", class_="tgme_widget_message_text js-message_text")
                    
                    #парсим данные с него
                    message = all_text.text
                        
                    #отправляем сообщение
                    await bot.send_message(id_user, f"Сообщение из канала {name_channel} {channel}\n\n{message}\n\nОпубликовано в {time}")
                    await sleep(1)

        #если это не канал
        else:
            await bot.send_message(id_user, f"Возможно, канала {channel} не существует, или это не канал\nКанал был помечен как не существующий и больше отслеживаться не будет")
            await ban_channel(channel)
            
    #если вышла ошибка
    except Exception as e:
        logging.error(f"{str(e)}")
        logging.error(str(traceback.format_exc()))
        await bot.send_message(id_user, f"[!] Тех. ошибка\n\nВозможно, канала {channel} не существует, или это не канал\nКанал был помечен как не существующий и больше отслеживаться не будет")
        await ban_channel(channel)


if __name__ == '__main__':
    asyncio.run(main())