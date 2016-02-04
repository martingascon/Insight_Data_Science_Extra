from flask import render_template
from app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
from a_Model import ModelIt

user = 'postgres' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'tweet'
my_password = 'po$t'

db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, host='localhost', user = user, password=my_password)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                             
                SELECT * FROM twitter WHERE delivery_method='Cesarean'\
;                                                                               
                """
    query_results = pd.read_sql_query(sql_query,con)
    query_results.head(5)
    births = ""
    print query_results[:10]
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births

@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT index, tweet_text, birth_month FROM twitter WHERE delivery_method='Cesarean';
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['tweet_text'], birth_month=query_results.iloc[i]['birth_month']))
    return render_template('cesareans.html',births=births)

@app.route('/input')
def cesareans_input():
    return render_template("input.html")


@app.route('/output')
def cesareans_output():
  #pull 'birth_month' from input field and store it
  patient = request.args.get('birth_month')
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
  query = "SELECT index, tweet_text, birth_month FROM twitter WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
  print query
  query_results=pd.read_sql_query(query,con)
  print query_results
  births = []
  for i in range(0,query_results.shape[0]):
      births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['tweet_text'], birth_month=query_results.iloc[i]['birth_month']))
      the_result = ''
  #the_result = ModelIt(patient,births)
  return render_template("output.html", births = births, the_result = the_result)
