from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
import asyncio
from config import TOKEN_BOT
from updateDB import add_channel, remove_channel, delete_all_channel_from_user


bot = Bot(token=TOKEN_BOT)
dp = Dispatcher()


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
                await add_channel(channel, message)
                valid_list_channel.append(channel)
            elif channel[0:13] == "https://t.me/":
                await add_channel("@"+channel[13:], message)
                valid_list_channel.append(channel)
            else:
                invalid_list_channel.append(channel)
        valid = ''
        invalid = ''
        if len(valid_list_channel)>0:
            valid = ' '.join(e for e in valid_list_channel)
        if len(invalid_list_channel)>0:
            invalid = ' '.join(e for e in invalid_list_channel)
        if len(valid)>0:
            await bot.send_message(message.from_user.id, f"Вы успешно отслеживаете каналы: {valid}")
        if len(invalid)>0:
            await bot.send_message(message.from_user.id, f"Не смог найти каналы: {invalid}")
                

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
                await remove_channel(channel, message)
                valid_list_channel.append(channel)
            elif channel[0:13] == "https://t.me/":
                await remove_channel("@"+channel[13:], message)
                valid_list_channel.append(channel)
            else:
                invalid_list_channel.append(channel)
        valid = ''
        invalid = ''
        if len(valid_list_channel)>0:
            valid = ' '.join(e for e in valid_list_channel)
        if len(invalid_list_channel)>0:
            invalid = ' '.join(e for e in invalid_list_channel)
        if len(valid)>0:
            await bot.send_message(message.from_user.id, f"Вы успешно отказались от подписки на каналы: {valid}")
        if len(invalid)>0:
            await bot.send_message(message.from_user.id, f"Не смог найти каналы: {invalid}")
    

@dp.message(F.text.startswith("/delete"))
async def delete(message: Message):
    await delete_all_channel_from_user(message.from_user.id)
    await bot.send_message(message.from_user.id, "Все подписки успешно удалены")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

