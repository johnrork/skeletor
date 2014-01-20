from flask import Flask, render_template, session, request, redirect, url_for
import datetime

app = Flask(__name__)
app.debug = True
app.user = 'johnrork'
app.secret_key = 'sekrit'


def valid_login():
	if 'logged_in' in session and (
			session['logged_in'] >
			datetime.datetime.now() - 
			datetime.timedelta(days=1)):
		return True 
	return False


@app.before_request
def check():
	if not ('login' in request.path or 'logout' in request.path) and not valid_login():
		return redirect(url_for('login'))


@app.route('/macros')
def list():
	l =[{'foo':'bar', 'bar': 'baz'}, {'foo':'bar', 'bar': 'baz'}]
	cols = ['foo', 'bar']
	return render_template('macros.html', list=l, c=cols)


@app.route('/')
def home():
	return 'hi'


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] == app.user:
			session['logged_in'] = datetime.datetime.now()	
			return 'success'
		else:
			return 'fail'
	return render_template('login.html')


@app.route('/logout')
def logout():
	if 'logged_in' in session:
		session.pop('logged_in')
	return 'logout'


if __name__ == '__main__':
	app.run()
