from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from dropdown_tables import *
from elasticsearch import Elasticsearch
import os

global admin_logged_on

dropdowns = create_engine('sqlite:///dropdowns.db', echo=True) 

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
es = Elasticsearch([{'host': 'localhost', 'port': 10000}])

class ReusableForm(Form):
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

    ped_opts_tuple  = []
    fab_opts_tuple = []
    post_opts_tuple = []
    test_opts_tuple =[]

    for x in ped_opts:
        temp = (x, x)
        ped_opts_tuple.append(temp)
    
    for x in fab_opts:
        temp = (x, x)
        fab_opts_tuple.append(temp)

    for x in post_opts:
        temp = (x, x)
        post_opts_tuple.append(temp)

    for x in test_opts:
        temp = (x, x)
        test_opts_tuple.append(temp)
    

    pedigree = SelectField('Pedigree:', choices=ped_opts_tuple)
    fabrication = SelectField('Fabrication:', choices=fab_opts_tuple)
    post_processing = SelectField('Post-Processing:', choices=post_opts_tuple)
    testing = SelectField('Testing:', choices=test_opts_tuple)
    search = StringField('')
    

def reformat(item):
    temp = item.replace("_", " ")
    temp = temp.split(" ")
    result = ""
    for word in temp:
        result += word[0].upper() + word[1::] + " "
    return result


def run_query(search):
    results = []
    search_command = {
                    "query": {
                        "bool": {
                        "should": [
                            { "query_string": { "query": search.data['search']}},
                            { "match": { "pedigree": search.data['pedigree'] }},
                            { "match": { "fabrication": search.data['fabrication']}},
                            { "match": { "post_processing": search.data['post_processing']}},
                            { "match": { "testing": search.data['testing']}}
                        ]
                        }
                    }
                    }
    results = es.search(index="database", body=search_command)
    doc_results = []
    doc_id = []
    if results:
        filters_applied = search.data['pedigree'] + " " +  search.data['fabrication'] + " " + search.data['post_processing'] + " " + search.data['testing']
        flash("You Searched for: " + search.data['search'] + " with filters: " + filters_applied)
        # print(results)
        if results['hits']['total'] == 0:
            flash("No Results")
        else:
            display_results = ''
            flash("Results:")
            for hit in results['hits']['hits']:
                doc_id.append('Document id: ' + hit['_id'])
                for item in hit['_source']:
                    display_results += item + ": " + hit['_source'][item] + '\n'
                # flash(str(display_results))
                # print(str(display_results))
                doc_results.append(display_results)
            return zip(doc_id, doc_results)

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
        search = ReusableForm(request.form)
        if request.method == 'POST':
            return search_results_admin(search)
            
        return render_template('admin_home.html', form=search)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return home()
    else:
        search = ReusableForm(request.form)
        if request.method == 'POST':
            return search_results(search)
            
    return render_template('front_page.html', form=search)

@app.route('/results_admin')
def search_results_admin(search):
    if admin_logged_on:
        my_results = run_query(search)
        return render_template('admin_home.html', form=search, results=my_results)
    else:
        return home()

@app.route('/Document', methods=['GET', 'POST'])
def display_document():
    doc_id = request.args.get('type')
    doc_id = doc_id.strip("Document id: ")
    search = {
                "query": {
                    "match": {
                        "_id": doc_id
                    }
                }
            }
    results = es.search(index='database', body=search)
    items = []
    display_results = []
    for hit in results['hits']['hits']:
        for item in hit['_source']:
            display_results.append(hit['_source'][item] + '\n')
            items.append(reformat(item))
            
    return render_template('/document.html', results=zip(items, display_results), doc_id=doc_id)

@app.route('/results')
def search_results(search):
    my_results = run_query(search)
    return render_template('front_page.html', form=search, results=my_results)

@app.route('/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('http://localhost:4000/search')



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
        admin_logged_on = False
    return home()


@app.route("/logout")
def logout():
    global admin_logged_on
    admin_logged_on = False
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
