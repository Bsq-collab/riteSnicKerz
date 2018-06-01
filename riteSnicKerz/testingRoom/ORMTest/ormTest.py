import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


player_day_assoc = db.Table(
    'Player Dates',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
    db.Column('day_id', db.Integer, db.ForeignKey('day.id'))
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(128))
    email = db.Column(db.String(128))
    days = relationship(Day, secondary=player_day_assoc, backref='players')


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daystamp = db.Column(db.Date, unique=True)

'''
day.players.all()
player.days.all()

To create new models and link them up, you'll have to do something like this:

player = Player()
day = Day()

player.days.append(day)
'''