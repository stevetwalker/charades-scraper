"""Create unlimited charades clues to use for salad bowl"""

import requests
import random
from peewee import fn
from model import Charades, Rooms


def get_charade():
    """Scrape charade from PlayCharades.net"""
    url = "http://www.playcharades.net/wp-content/themes/canvas-child/pc_word.php"

    # cat_id 1, 2, 3 and 11 correspond to easy, medium, difficult and phrases
    request = {"cat_id": random.choice([1, 2, 3, 11])}
    charade = requests.post(url, request).content.decode("utf-8")
    return charade

def create_charades(room, number):
    """Create the charades to use for this game."""
#    room = Rooms(name=room)
#    room.save()
    while Charades.select().where(Charades.room == room).count() < number:
        try:
            charade = get_charade()
            # If that charade isn't already in the room, add it to db
            query = Charades.get_or_none(Charades.charade == charade, Charades.room == room)
            if query is None:
                charade = Charades(room=room, charade=charade)
                charade.save()
        except:
            pass

def give_charade(room):
    """Return random unguessed charade."""

    # Count how many unguessed charades remain
    countdown = Charades.select()\
        .where(Charades.room == room, Charades.guessed == False).count()

    # If no unguessed charade remain, reset all charades to guessed=False
    if countdown == 0:
        Charades.update({Charades.guessed: False})\
            .where(Charades.room == room).execute()
        countdown = Charades.select()\
            .where(Charades.room == room, Charades.guessed == False).count()

    # Randomly choose one unguessed charade to deliver
    charade = Charades.select()\
        .where(Charades.room == room, Charades.guessed == False)\
        .order_by(fn.Random()).limit(1)

    charade = [charade.charade for charade in charade][0]

    return charade, countdown - 1
