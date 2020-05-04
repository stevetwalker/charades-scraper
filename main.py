"""Two-person salad bowl game."""

import random
import os

from flask import Flask, render_template, request, redirect, url_for, session
#from playhouse.db_url import connect
from model import Charades, Rooms, db

import charades_scraper


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/start', methods=['GET', 'POST'])
def start():
    """Get game parameters (room name and number of clues) and populate DB."""
    if request.method == 'POST':
        session['room'] = request.form['room']
        if Charades.get_or_none(Charades.room == session['room']) is not None:
            return render_template('start.jinja2', room_exists_error="Room already exists.")

        else:
            charades_scraper.create_charades(request.form['room'],
                                             int(request.form['number']))
            return redirect(url_for('next_turn', room=session['room']))

    return render_template('start.jinja2', session=session, error=None)

@app.route('/play/<room>', methods=['GET', 'POST'])
def play(room):
    """Show one clue at a time until all clues have been given."""

    # If the player got the last clue, mark as guessed
    if request.form['btn'] == "Next clue":
        Charades.update({Charades.guessed: True})\
            .where(Charades.room == room, Charades.charade == session.get('clue')).execute()

    # Get a new clue
    charade, countdown = charades_scraper.give_charade(room)
    session['clue'] = charade

    if request.method == 'POST':
        return render_template('play.jinja2', charade=charade, countdown=countdown, room=session['room'])

    return render_template('play.jinja2', charade=charade, countdown=countdown, room=session['room'], clue=session['clue'])

@app.route('/next-turn/<room>', methods=['GET', 'POST'])
def next_turn(room):
    """Show a holding screen until the player begins their turn."""
    if Charades.get_or_none(Charades.room == room) is None:
        return redirect(url_for('start', no_room_error="Room does not exist."))
    return render_template('next-turn.jinja2', room=session['room'])

if __name__ == "__main__":
#    db.connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))
    db.drop_tables([Charades])
    db.create_tables([Charades])
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
