import os
from model import db, Charades
from playhouse.db_url import connect

db.connect()
db.create_tables([Charades])
