import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

subs = db.Table('subs',
	db.Column('user_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('channel_id',db.Integer,db.ForeignKey('channel.channel_id'))
)

class User(db.Model):
	user_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20))
	subscriptions = db.relationship('Channel',secondary=subs,backref=db.backref('subscribers',lazy = 'dynamic'))

class Channel(db.Model):
	channel_id = db.Column(db.Integer, primary_key = True)
	channel_name = db.Column(db.String(20))

#example command:

#$ *channel*.subscribers.append(*user*)