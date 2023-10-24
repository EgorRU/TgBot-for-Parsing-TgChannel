from aiogram import Bot
from config import TOKEN_BOT
import requests, time, asyncio
from updateDB import select_id, select_channel, ban_channel


bot = Bot(token=TOKEN_BOT)


async def main():
    while True:
        list_id_user = select_id()
        for id_user in list_id_user:
            list_channel_from_user = select_channel(id_user)
            for channel in list_channel_from_user:
                try:
                    response = requests.get(f"https://t.me/s/{channel[1:]}").text[-250:]
                    await bot.send_message(id_user, f"Сообщение из {channel}\n\n{response}")
                except:
                    await bot.send_message(id_user, "Возможно, такого канала больше нет")
                    await ban_channel(channel)
        time.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())