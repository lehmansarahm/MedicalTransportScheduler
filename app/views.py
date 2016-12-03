from flask import render_template
from app import app
from .forms import LoginForm

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',title='Home')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/schedule')
def schedule():
	return render_template('schedule.html',title='Driving Schedule')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@app.route('/reports')
def reports():
	return render_template('reports.html',title='Scheduler Reports')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#@app.route('/login',methods=['GET','POST'])
#def login():
#	form = LoginForm()
#	if form.validate_on_submit():
#		flash('Login requested for OpenID="%s", remember_me=%s' % (form.openid.data, str(form.remember_me.data)))
#		return redirect('/index')
#	return render_template('login.html',title='Sign In',form=form,providers=app.config['OPENID_PROVIDERS'])