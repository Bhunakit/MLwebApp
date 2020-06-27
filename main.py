from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from secondary import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix='')
app.config['SECRET_KEY'] = 'b91a77d1ed4b44aa71ab1a740f565e13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class contacts(db.Model):
	_id = db.Column('id', db.Integer, primary_key=True)
	email_data = db.Column(db.String(100))
	content_data = db.Column(db.String(100))

	def __init__(self, email_data, content_data):
		self.email_data = email_data
		self.content_data = content_data

@app.route('/')
def home():
	if 'email' in session:
		user = session['email'].split('@')[0].upper()
		return render_template('home.html', user=user)
	return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	email = None
	if request.method == 'POST':
		session.permanent = True
		email = request.form['email']
		content = request.form['content']
		session['email'] = email

		found_contact = contacts.query.filter_by(email_data=email, content_data=content).first()
		if found_contact:
			session['email'] = found_contact.email_data
		else:
			cont = contacts(email, content)
			db.session.add(cont)
			db.session.commit()

		flash('Query Recieved')
		return render_template('contact.html', query=True, email=email)
	else:
		if 'email' in session:
			email = session['email']
		return render_template('contact.html', email=email)

@app.route('/about', methods=['GET', 'POST'])
def about():
	if request.method == 'POST':
		return render_template()
	return render_template('about.html')

@app.route('/clearsession')
def clearsession():
	if 'email' in session:
		session.pop('email', None)
		flash('Session Cleared')
	return redirect(url_for('home'))

if __name__ == '__main__':
	db.create_all()
	app.run(port=5000, debug=True)
