## Установка и запуск на Windows
- git clone https://github.com/EgorRU/TgBot-for-Parsing-TgChannel
- cd TgBot-for-Parsing-TgChannel
- pip install -r requirements.txt
- py main.py

## Команды для бота
- /add <item> - добавить список отслеживаемых каналов
- /remove <item> - удалить список отслеживаемых каналов
- /delete - удалить все отслеживаемые каналы

## Примечание
- После обновления списка каналов нужно перезапустить бота
- Создать файл config.py
Его содержимое: 
TOKEN_BOT = ""
API_ID = ""
API_HASH = ""
TARGET_CHANNEL = "id канала, куда будут пересылаться сообщения, нужно быть админом канала"
