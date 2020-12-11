import sqlalchemy as db
engine = db.create_engine('sqlite:///FeedbackBot.db')
connection = engine.connect()
metadata = db.MetaData()
census = db.Table('server', metadata, autoload=True, autoload_with=engine)

def push_data(guild,label,channel,min_length):
    try:
       query = db.insert(census).values(guild=guild, label=label, channel=channel, min_length=min_length)
       insert = connection.execute(query)
    except:
       query = db.update(census).where(guild==guild).values(label=label, channel=channel, min_length=min_length)
       insert = connection.execute(query)
def get_data(guild):
    query = db.select([census]).where(guild == guild)
    data = connection.execute(query).fetchall()
    print(query,data)
    return data
