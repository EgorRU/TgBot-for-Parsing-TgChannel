import sqlite3

async def connection_db():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    create_db = 'CREATE TABLE IF NOT EXISTS data(channel TEXT, primary key(channel))'
    base.execute(create_db)
    base.commit()
    return base, cur
    

async def add_channel(channel):
    base, cur = await connection_db()
    data = cur.execute("SELECT channel FROM data where channel=?", (channel,)).fetchone()
    if data == None:
        cur.execute("INSERT INTO data values(?)", (channel,))
        base.commit()
    base.close()


async def remove_channel(channel):
    base, cur = await connection_db()
    cur.execute("DELETE from data where channel=?", (channel,))
    base.commit()
    base.close()


async def delete_all_channel():
    base, cur = await connection_db()
    cur.execute("DELETE from data")
    base.commit()
    base.close()


async def select_channel():
    base, cur = await connection_db()
    channels = cur.execute("SELECT channel FROM data").fetchall()
    base.close()
    list_channel = []
    for channel in channels:
        list_channel.append(channel[0])
    return list_channel
