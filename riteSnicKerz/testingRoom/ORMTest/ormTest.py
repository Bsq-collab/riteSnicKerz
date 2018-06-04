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
	subscriptions = db.relationship('Channel',secondary=subs,backref=db.backref('subscribers'))
	#Note on secondary
	#Tells helper table - hey use this table for connecting to the Channel so you can do stuff to it. 
	#Note on backref
	#Its basically saying: Hey Channel youre gonna have another variable and its gonna be called subscribers. It'll be a list of subscribers

class Channel(db.Model):
	channel_id = db.Column(db.Integer, primary_key = True)
	channel_name = db.Column(db.String(20))

#example command:

#$ *channel*.subscribers.append(*user*)

if __name__ == '__main__':
	db.create_all()
	user1=User(name="bob")
	if user1.query.filter_by(name="bob").first() is not None:
		os.system("rm school.sqlite3")

	user2=User(name="jay")
	channel1=Channel(channel_name="Vanoss")
	channel2=Channel(channel_name="SlowMoGuys")
	channel1.subscribers.append(user1)
	print "CHANNEL 1 SUBSCRIBERS"
	print channel1.subscribers
	print "DONE"
	user2.subscriptions.append(channel2)
	user2.subscriptions.append(channel1)

	print "SUBSCRIPTIONS OF USER 2"
	print user2.subscriptions
	print "DONE"
	db.session.add(user1)
	db.session.add(user2)
	db.session.add(channel1)
	db.session.add(channel2)
	db.session.commit()

	app.run(debug = True, use_reloader=False)
