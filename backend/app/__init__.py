from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS

mysql = MySQL()

def createApp():
	app = Flask(__name__)

	# mysql config

	app.config["MYSQL_HOST"] = 'bz6uyriuwkoupt9fm9ty-mysql.services.clever-cloud.com'
	app.config["MYSQL_USER"] = 'uncmne6nhlsj7wjz'
	app.config["MYSQL_PASSWORD"] = 'cJaYyf1WT3Bw1xESmLBO'
	app.config["MYSQL_DB"] = 'bz6uyriuwkoupt9fm9ty'

	mysql.init_app(app)
	CORS(app)

	from .routes import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app
