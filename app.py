from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from dropdown_tables import *

global admin_logged_on
dropdowns = create_engine('sqlite:///dropdowns.db', echo=True) 

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


@app.route('/', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return home()
    else:
        return redirect('http://localhost:4000/admin_home')

@app.route('/admin_home', methods=['GET', 'POST'])
def admin_home():
    if not session.get('logged_in') or not admin_logged_on:
        return home()
    else:
        if request.method == 'POST':
            if request.form['admin_option'] == 'search':
                return redirect('http://localhost:4000/admin_search')

            elif request.form['admin_option'] == 'add_info':
                pass
                
        return render_template('admin_front_page.html')
        


@app.route('/login', methods=['POST'])
def login():
    global admin_logged_on
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=dropdowns)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()

    if result and result.admin:
        session['logged_in'] = True
        admin_logged_on = True
        return admin()

    elif result:
        session['logged_in'] = True
        admin_logged_on = False
    else:
        flash('wrong password!')
        admin_logged_on = False
    return home()
 
@app.route("/logout")
def logout():
    global admin_logged_on
    admin_logged_on = False
    session['logged_in'] = False
    return home()


@app.route('/search', methods=['GET', 'POST'])


def search():
    if not session.get('logged_in'):
        return home()
    form = ReusableForm(request.form)
    Session = sessionmaker(bind=dropdowns)
    a = Session()

    ped_opts_q = a.query(Drop_ped.ped)
    fab_opts_q = a.query(Drop_fab.fab)
    post_opts_q = a.query(Drop_post.post)
    test_opts_q = a.query(Drop_test.test)

    ped_opts = convert_str(ped_opts_q)
    fab_opts = convert_str(fab_opts_q)
    post_opts = convert_str(post_opts_q)
    test_opts = convert_str(test_opts_q)

 
    print (form.errors)
    if request.method == 'POST':
        pedigree=request.form['pedigree']
        fabrication=request.form['fabrication']
        post_processing=request.form['post_processing']
        testing=request.form['testing']
        print (pedigree, " ", fabrication, " ", post_processing, " ", testing)

    return render_template('front_page.html', form=form, ped_list=ped_opts, fab_list=fab_opts, post_list=post_opts, test_list=test_opts)

@app.route('/admin_search', methods=['GET', 'POST'])
def admin_search():
    if not session.get('logged_in') or not admin_logged_on:
        return home()
    form = ReusableForm(request.form)
    Session = sessionmaker(bind=dropdowns)
    a = Session()

    ped_opts_q = a.query(Drop_ped.ped)
    fab_opts_q = a.query(Drop_fab.fab)
    post_opts_q = a.query(Drop_post.post)
    test_opts_q = a.query(Drop_test.test)

    ped_opts = convert_str(ped_opts_q)
    fab_opts = convert_str(fab_opts_q)
    post_opts = convert_str(post_opts_q)
    test_opts = convert_str(test_opts_q)

 
    print (form.errors)
    if request.method == 'POST':
        if request.form["admin_option"] == "add_info":
            return redirect("http://localhost:4000/admin_home")
        pedigree=request.form['pedigree']
        fabrication=request.form['fabrication']
        post_processing=request.form['post_processing']
        testing=request.form['testing']
        print (pedigree, " ", fabrication, " ", post_processing, " ", testing)

    return render_template('admin_search_page.html', form=form, ped_list=ped_opts, fab_list=fab_opts, post_list=post_opts, test_list=test_opts)

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
 
