from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
import asyncio
from config import TOKEN_BOT, API_ID, API_HASH, TARGET_CHANNEL
from updateDB import add_channel, remove_channel, delete_all_channel, select_channel


bot = Bot(token=TOKEN_BOT)
dp = Dispatcher()
user_bot = Client(name='me', api_id=API_ID, api_hash=API_HASH)


@dp.message(F.text == '/start')
async def start(message: Message):
    await bot.send_message(message.from_user.id, "Добро пожаловать!!!\n\nЧтобы получать сообщения из ПУБЛИЧНЫХ каналов, напишите /add и список ПУБЛИЧНЫХ каналов через пробел.\n\nЧтобы убрать отслеживание ПУБЛИЧНЫХ каналов, напишите /remove и список ПУБЛИЧНЫХ каналов через пробел.\n\nЧтобы удалить все подписки, напишите /delete\n\n\nКаналы указывать в виде @username_channel или https://t.me/....")


@dp.message(F.text.startswith("/add"))
async def add(message: Message):
    channel_array = message.text.split()
    if len(channel_array)==1:
        await bot.send_message(message.from_user.id, "Укажите после команды /add все ПУБЛИЧНЫЕ каналы через пробел, от которых хотите получать сообщения\n\nКаналы указывать в виде @username_channel или https://t.me/....")
    else:
        invalid_list_channel = []
        valid_list_channel = []
        channel_array.pop(0)
        for channel in channel_array:
            if channel[0]=="@":
                await add_channel(channel)
                valid_list_channel.append(channel)
            elif channel[0:13] == "https://t.me/":
                await add_channel("@"+channel[13:])
                valid_list_channel.append("@"+channel[13:])
            else:
                invalid_list_channel.append(channel)
        valid = ''
        invalid = ''
        if len(valid_list_channel)>0:
            valid = ' '.join(e for e in valid_list_channel)
        if len(invalid_list_channel)>0:
            invalid = ' '.join(e for e in invalid_list_channel)
        if len(valid)>0:
            await bot.send_message(message.from_user.id, f"Вы успешно отслеживаете каналы:\n{valid}")
        if len(invalid)>0:
            await bot.send_message(message.from_user.id, f"Не смог найти каналы:\n{invalid}")
                

@dp.message(F.text.startswith("/remove"))
async def remove(message: Message):
    channel_array = message.text.split()
    if len(channel_array)==1:
        await bot.send_message(message.from_user.id, "Укажите после команды /remove все ПУБЛИЧНЫЕ каналы, от которых не желаете получать сообщения\n\nКаналы указывать в виде @username_channel или https://t.me/....")
    else:
        invalid_list_channel = []
        valid_list_channel = []
        channel_array.pop(0)
        for channel in channel_array:
            if channel[0]=="@": 
                await remove_channel(channel)
                valid_list_channel.append(channel)
            elif channel[0:13] == "https://t.me/":
                await remove_channel("@"+channel[13:])
                valid_list_channel.append("@"+channel[13:])
            else:
                invalid_list_channel.append(channel)
        valid = ''
        invalid = ''
        if len(valid_list_channel)>0:
            valid = ' '.join(e for e in valid_list_channel)
        if len(invalid_list_channel)>0:
            invalid = ' '.join(e for e in invalid_list_channel)
        if len(valid)>0:
            await bot.send_message(message.from_user.id, f"Вы успешно отказались от подписки на каналы:\n{valid}")
        if len(invalid)>0:
            await bot.send_message(message.from_user.id, f"Не смог найти каналы:\n{invalid}")
    

@dp.message(F.text.startswith("/delete"))
async def delete(message: Message):
    await delete_all_channel()
    await bot.send_message(message.from_user.id, "Все подписки успешно удалены")


async def new_post(client, message):
    await message.forward(chat_id=TARGET_CHANNEL)


async def bot_polling():
    await dp.start_polling(bot)


async def start_user_bot():
    user_bot = Client(name='me', api_id=API_ID, api_hash=API_HASH)
    name_channel = await select_channel()
    user_bot.add_handler(MessageHandler(new_post, filters.chat(chats=name_channel)))
    await user_bot.start()
    await idle()
    

async def main():
    task1 = asyncio.create_task(start_user_bot())
    task2 = asyncio.create_task(bot_polling())
    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())