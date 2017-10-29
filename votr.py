from flask import Flask
from models import db 

votr = Flask(__name__)

votr.config.from_object('config') 

db.init_app(votr)
db.create_all(app=votr)

@votr.route('/')
def home():
	return 'hello'


if __name__=='__main__':
	votr.run()