from flask import (
	Flask, render_template, request, flash, redirect, url_for, session
	)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users

votr = Flask(__name__)

# load config from the config.py
votr.config.from_object('config') 

# create db
db.init_app(votr)
db.create_all(app=votr)

@votr.route('/')
def home():
	return render_template('index.html')


@votr.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		# get info from the form
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']

		password = generate_password_hash(password)

		user = Users(email=email, username=username, password=password)

		db.session.add(user)
		db.session.commit()

		flash('Thank you for signup, please login')
		return redirect(url_for('home'))

	# for GET request, just render the template
	return render_template('signup.html')


@votr.route('/login', methods=['POST'])
def login():
	username=request.form['username']
	password=request.form['password']

	user = Users.query.filter_by(username=username).first()

	if user:
		password_hash = user.password

		if check_password_hash(password_hash, password):
			session['user']=username 
			flash('Login successfull')
	else:
		flash('Incorrect password or username', 'error')

	return redirect(url_for('home'))


@votr.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user')

		flash('See you again')
	return redirect(url_for('home'))


@votr.route('/api/polls', methods=['GET', 'POST'])
def api_polls():
	if request.method == 'POST':
		poll = request.get_json()

		return "The title of the poll is {} and the options are {} and {}".format(poll['title'], *poll['options'])
	else:
		all_polls = {}
		topics = Topics.query.all()
		for topic in topics:
			all_polls[topic.title] = {'options': [poll.option.name for poll in Polls.query.filter_by(topic=topic)]}
			
		return jsonify(all_polls)


@votr.route('/api/polls', methods=['GET', 'POST'])
def api_polls():
	if request.method == 'POST'
	poll = request.get_json()
	return

if __name__=='__main__':
	votr.run()