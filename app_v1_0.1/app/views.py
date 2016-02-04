from flask import render_template
from app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from flask import request
#from a_Model import ModelIt

user = 'postgres' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'crime'

db = create_engine('postgres://%s/%s'%(host,dbname))
con = None
con = psycopg2.connect(database = dbname, host='localhost', user = user)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Crime-Corruption Twitter Maps', user = { 'nickname': 'Mart' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                             
                SELECT * FROM tweet;                                                                             
                """
    query_results = pd.read_sql_query(sql_query,con)
    print query_results[:10]
    

