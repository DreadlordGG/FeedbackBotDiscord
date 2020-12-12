import sqlalchemy as db
engine = db.create_engine('sqlite:///backends/FeedbackBot.db')
connection = engine.connect()
metadata = db.MetaData()
census = db.Table('server', metadata, autoload=True, autoload_with=engine)

def push_data(guild,category,channel,min_length,max_feedback):
    try:
       query = db.insert(census).values(guild=guild, category=category, channel=channel, min_length=min_length,max_feedback=max_feedback)
       insert = connection.execute(query)
    except:
       query = db.update(census).where(guild==guild).values(category=category, channel=channel, min_length=min_length,max_feedback=max_feedback)
       insert = connection.execute(query)
def get_data(guild):
    query = db.select([census]).where(guild == guild)
    data = connection.execute(query).fetchall()
    return data
