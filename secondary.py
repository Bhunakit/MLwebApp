from flask import Blueprint, render_template, request, flash, redirect, url_for
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
import numpy as np

second = Blueprint('second', __name__, static_folder='static', template_folder='templates')

model = LinearRegression()

@second.route('/linreg', methods=['GET', 'POST'])
def linreg():
	if request.method == 'POST':
		x = list(map(int, request.form['x'].split()))
		y = list(map(int, request.form['y'].split()))
		x = np.array(x).reshape((-1, 1))
		model.fit(x, y)
		flash('Model Trained')
		return redirect('/linregpredict')
	return render_template('operations.html')

@second.route('/linregpredict', methods=['GET', 'POST'])
def linregpredict():
	if request.method == 'POST':
		num = float(request.form['num'])
		result = model.predict([[num]])
		flash(result)
		return render_template('operations.html')
	return render_template('operations.html')
