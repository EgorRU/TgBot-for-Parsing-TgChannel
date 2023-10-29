import sqlite3
import datetime
     

async def connection_db():
    base = sqlite3.connect("database.db")
    cur = base.cursor()
    create_db = '''
    CREATE TABLE IF NOT EXISTS data(id INTEGER, channel TEXT, fullname TEXT, username TEXT, last_time TEXT, state INTEGER, primary key(id, channel))
    '''
    base.execute(create_db)
    base.commit()
    return base, cur
    

async def add_channel(channel, message):
    base, cur = await connection_db()
    data = cur.execute("SELECT id, channel FROM data WHERE id=? and channel=?", (message.from_user.id, channel)).fetchone()
    if data == None:
        data_user = (message.from_user.id, channel, message.from_user.full_name, message.from_user.username, str(datetime.datetime.now())[:19], 1)
        cur.execute("INSERT INTO data values(?,?,?,?,?,?)", data_user)
        base.commit()
    base.close()


async def remove_channel(channel, message):
    base, cur = await connection_db()
    data = cur.execute("SELECT id, channel FROM data WHERE id=? and channel=?", (message.from_user.id, channel)).fetchone()
    if data != None:
        cur.execute(f"DELETE from data where id=? and channel=?", (message.from_user.id, channel))
        base.commit()
    base.close()


async def delete_all_channel_from_user(id_user):
    base, cur = await connection_db()
    cur.execute(f"DELETE from data where id={id_user}")
    base.commit()
    base.close()
    

async def select_id():
    base, cur = await connection_db()
    data = cur.execute("SELECT id FROM data").fetchall()
    base.close()
    set_user = set()
    for e in data:
        set_user.add(e[0])
    return list(set_user)


async def select_channel(id_user):
    base, cur = await connection_db()
    data = cur.execute(f"SELECT channel FROM data WHERE id=? and state=?", (id_user, 1)).fetchall()
    base.close()
    set_channel = set()
    for e in data:
        set_channel.add(e[0])
    return list(set_channel)


async def ban_channel(channel):
    base, cur = await connection_db()
    cur.execute(f"UPDATE data set state=? where channel=?",(0, channel))
    base.commit()
    base.close()
