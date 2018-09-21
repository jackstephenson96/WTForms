from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators


import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
	return "Hello, world!"
	
#create class to represent WTForm that inherits flask form
class iTunesForm(FlaskForm):
	artist_name = StringField('Artist name?', validators=[validators.Required()])
	numresults = IntegerField('How many results?', validators=[validators.Required()])
	email = StringField('What is your email?', validators=[validators.Required(), validators.Email()])
	submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
	#what code goes here?
	itunesform = iTunesForm()
	return render_template('itunes-form.html', form=itunesform) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
	#what code goes here?
	form = iTunesForm(request.form)
	params = {}
	song = {}
	results_python = []
	if request.method == 'POST' and form.validate_on_submit():
		params['term'] = form.artist_name.data
		params['limit'] = form.numresults.data
		baseurl = 'https://itunes.apple.com/search'
		r = requests.get(baseurl, params=params, headers={"Accept":"application/json"})
		response_json = json.loads(r.text)['results']
		results_python = response_json

		# HINT : create itunes-results.html to represent the results and return it
		return render_template('itunes-result.html', results_html=results_python)
	flash('All fields are required!')
	return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
	app.run()
