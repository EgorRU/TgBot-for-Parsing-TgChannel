import asyncio
from parsing import parsing
from bot_polling import bot_polling


async def main():
    task1 = asyncio.create_task(parsing())
    task2 = asyncio.create_task(bot_polling())
    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())