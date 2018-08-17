from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from dropdown_tables import *

dropdowns = create_engine('sqlite:///dropdowns.db', echo=True) ###

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    pedigree = TextField('Pedigree:', validators=[validators.required()])
    fabrication = TextField('Fabrication:', validators=[validators.required()])
    post_processing = TextField('Post-Processing:', validators=[validators.required()])
    testing = TextField('Testing:', validators=[validators.required()])
 
 

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
    	return redirect('http://localhost:4000/search')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=dropdowns)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = ReusableForm(request.form)
    Session = sessionmaker(bind=dropdowns)
    a = Session()

    ped_opts = a.query(Drop_ped.ped)
    fab_opts = a.query(Drop_fab.fab)
    post_opts = a.query(Drop_post.post)
    test_opts = a.query(Drop_test.test)
 
    print (form.errors)
    if request.method == 'POST':
        pedigree=request.form['pedigree']
        fabrication=request.form['fabrication']
        post_processing=request.form['post_processing']
        testing=request.form['testing']
        print (pedigree, " ", fabrication, " ", post_processing, " ", testing)

    return render_template('front_page.html', form=form, ped_list=ped_opts, fab_list=fab_opts, post_list=post_opts, test_list=test_opts)

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
 
