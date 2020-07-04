from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from secondary import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix='')
app.config['SECRET_KEY'] = 'b91a77d1ed4b44aa71ab1a740f565e13'
app.permanent_session_lifetime = timedelta(days=1)


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

        flash('Sorry cannot accept query right now. Please contact us at example@gmail.com')
        return render_template('contact.html', query=True, email=email)
    else:
        if 'email' in session:
            email = session['email']
        return render_template('contact.html', email=email)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/clearsession')
def clearsession():
    if 'email' in session:
        session.pop('email', None)
        flash('Session Cleared')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=8080, debug=True)
