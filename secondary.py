from flask import Blueprint, render_template, request, flash
from sklearn.ensemble import RandomForestClassifier
import numpy as np

second = Blueprint('second', __name__, static_folder='static', template_folder='templates')

@second.route('/operations', methods=['GET', 'POST'])
def operations():
	if request.method == 'POST':
		result = float(request.form['num1']) * float(request.form['num2']) 
		flash(result)
		return render_template('operations.html')
	return render_template('operations.html')

