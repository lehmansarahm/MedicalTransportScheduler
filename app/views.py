from flask import render_template
from app import app

import requests
from requests.auth import HTTPDigestAuth
import json

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',title='Home')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/upload')
def upload():
	return render_template('upload.html',title='Upload Data')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/configure')
def configure():
	return render_template('configure.html',title='Configure Schedule')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/confirm')
def confirm():
	return render_template('confirm.html',title='Confirm Schedule')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/schedule')
def schedule():
	# Replace with the correct URL
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&key=AIzaSyDQsoQIu0YpgcyoC_N-X6MdWWmYM36bTts"

	# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
	myResponse = requests.get(url)
	#print (myResponse.status_code)

	# For successful API call, response code will be 200 (OK)
	if(myResponse.ok):

	    # Loading the response data into a dict variable
	    # json.loads takes in only binary or string variables so using content to fetch binary content
	    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
	    jData = json.loads(myResponse.content)

	    # total number of properties in the response - destinations, origins, rows, status
	    print("The response contains {0} properties".format(len(jData)))

	    origins = jData['origin_addresses']
	    destinations = jData['destination_addresses']

	    # total number of path groups by destination
	    rows = jData['rows']
	    print("The response contains {0} rows".format(len(rows)))

	    # individual possible paths from each origin for the given destination
	    rowNum = len(rows)
	    for i in range(0, rowNum):
	    	row = rows[i]
	    	elements = row['elements']
	    	print("Row {0} has {1} elements".format(i,len(elements)))
	else:
	  # If response code is not ok (200), print the resulting http error code with description
	    myResponse.raise_for_status()
	return render_template('schedule.html',title='Driving Schedule')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/reports')
def reports():
	return render_template('reports.html',title='Scheduler Reports')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/reportPatientTrips')
def reportPatientTrips():
	return render_template('reportPatientTrips.html',title='Report:  Patient Trips in Last 30 Days')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/reportDriverTrips')
def reportDriverTrips():
	return render_template('reportDriverTrips.html',title='Report:  Driver Trips in Last 30 Days')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/reportDriverHours')
def reportDriverHours():
	return render_template('reportDriverHours.html',title='Report:  Driver Active Hours in Last 30 Days')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#@app.route('/login',methods=['GET','POST'])
#def login():
#	form = LoginForm()
#	if form.validate_on_submit():
#		flash('Login requested for OpenID="%s", remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
#		return redirect('/index')
#	return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])