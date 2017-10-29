from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Base(db.Model):
	__abstract__=True 

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp())


class Topics(Base):
	title = db.Column(db.String(500))

	def __repr__(self):
		return self.title 


class Options(Base):
	name = db.Column(db.String(200))


class Polls(Base):
	topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
	option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
	vote_count = db.Column(db.Integer, default=0)
	status = db.Column(db.Boolean)
	topic = db.relationship('Topics', foreign_keys=[topic_id],
		backref=db.backref('options', lazy='dynamic'))
	option = db.relationship('Options', foreign_keys=[option_id]) 

	def __repr__(self):
		return self.option.name 
