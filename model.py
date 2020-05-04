from peewee import Model, CharField, DateTimeField, ForeignKeyField, BooleanField
import os

from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))

class BaseModel(Model):
    class Meta:
        database = db

# Currently unused
class Rooms(BaseModel):
    name = CharField(max_length=255, unique=True)

class Charades(BaseModel):
    charade = CharField(max_length=255)
    guessed = BooleanField(default=False)
    room = ForeignKeyField(Rooms, null=False)
