from flask import Flask, render_template, session, request, redirect, url_for
import datetime
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.user = {'username':'test', 'password': 'password'}
app.secret_key = 'sekrit'
app.results_per = 10
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Chinook_Sqlite_AutoIncrementPKs.sqlite'
db = SQLAlchemy(app)


class Album(db.Model):
	__table__ = db.Table('Album', db.metadata, autoload=True, autoload_with=db.engine)


def valid_login():
	if 'logged_in' in session and (
			session['logged_in'] >
			datetime.datetime.now() - 
			datetime.timedelta(days=1)):
		return True 
	return False


@app.before_request
def check():
	if not 'login' or 'logout' in request.path and not valid_login():
		return redirect(url_for('login'))


@app.route('/')
def home():
	return redirect(url_for('list'))


@app.route('/albums/')
@app.route('/albums/<int:page>/')
def list(page=1):
	data = Album.query

	if request.args.get('sort'):
		order = request.args.get('sort')
		if request.args.get('dir') == 'desc':
			order = db.desc(order)
		data = data.order_by(order)
	return render_template('list.html', 
							list=data.paginate(page), 
							cols=['Title'], 
							params=params)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if (request.form['username'] == app.user['username'] 
			and request.form['password'] == app.user['password']):
			session['logged_in'] = datetime.datetime.now()	
			return redirect(url_for('home'))
		else:
			return 'fail'
	return render_template('login.html')


@app.route('/logout')
def logout():
	if 'logged_in' in session:
		session.pop('logged_in')
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run()
