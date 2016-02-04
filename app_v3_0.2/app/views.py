from flask import render_template, jsonify
from app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import numpy as np
import psycopg2
from flask import request
from a_Model import ModelIt
from scipy import stats
import glob
import sys
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import silhouette_score
from sklearn.neighbors import KernelDensity
from sklearn.neighbors import KNeighborsRegressor
from sklearn.mixture import GMM
from sklearn.externals import joblib
import datetime as dt
from dateutil.relativedelta import relativedelta

user = 'postgres' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'gdelt_db'
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
                SELECT "DATE" FROM gdelt where "GEO_FULLNAME" LIKE 'Mexico';                                                                        
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
def output():
  #pull city from input
  req_city = request.args.get('city')
  weeks = request.args.get('weeks')

  print weeks  
  today = dt.date.today()
  print today
  d=[]

  if weeks=='W2':
    d = today - relativedelta(days=14)
  if weeks=='W3':
    d = today - relativedelta(days=21)
  if weeks=='W4':
    d = today - relativedelta(days=28)
  print d
  #just select the numart, lat and long of the indicated country were geo code is country and gtype = 4 
  query = "SELECT edate,numarts,geolat,geolon FROM gdelt where geocc LIKE '%s' and gtype>'3' and edate>= '2015-06-10' " % req_city
  
  # Let's print the resutls
  #print query
  # we pass query to a pandaframe
  query_results=pd.read_sql_query(query,con)
 
  ## print the results
  #print query_results

  # empty list with all the cities
  cities = []
  cities2 = []
  #for i in range(0,query_results.shape[0]):
  #    births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['tweet_text'], birth_month=query_results.iloc[i]['birth_month']))
  #the_result = ''
  #cities.appenddict(index=query_results.iloc[1]['index'], narts=query_results.iloc[1]['numarts'], date=query_results.iloc[1]['edate'])

  #print query_results
  for i in range(0,query_results.shape[0]):
  #    births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['tweet_text'], birth_month=query_results.iloc[i]['birth_month']))
      cities.append(dict(edate=query_results.iloc[i]['edate'], numarts=query_results.iloc[i]['numarts'], geolat=query_results.iloc[i]['geolat'], geolon=query_results.iloc[i]['geolon']))
      if (d<query_results.iloc[i]['edate'].date()):
        cities2.append(dict(edate=query_results.iloc[i]['edate'], numarts=query_results.iloc[i]['numarts'], geolat=query_results.iloc[i]['geolat'], geolon=query_results.iloc[i]['geolon']))

  #the_result = ModelIt(patient,births)
  #return render_template("output.html", births = births, the_result = the_result)
  
 
  mlat=query_results.loc[:,['geolat']].mean()
  mlon =query_results.loc[:,['geolon']].mean()
  #aux=[]
  print mlat,mlon

  lat = 22
  lon = -102
  lat_c = 23
  lon_c = -103
  kde_score_max = 0


  #print aux

  #mlat = aux.mean()


  #xmin = aux.min()
  #xmax = aux.max()
  #aux=[]

  #aux = query_results.loc[:,['geolon']]
  #mlon=aux.mean()
  #ymin = aux.min()
  #ymax = aux.max()
  #print xmin, xmax, ymin, ymax, mlat, mlon

  #X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
  #positions = np.vstack([X.ravel(), Y.ravel()])
  #values = np.vstack([query_results.loc[:,['geolat']], query_results.loc[:,['geolon']]])
  #kernel = stats.gaussian_kde(values)
  #kdepos = np.reshape(kernel(positions).T, X.shape)
  #print np.isnan(kdepos).any()
  #kdepos = np.nan_to_num(0)
  #print kdepos
  
  kdepos=0
  #fig = plt.figure()
  #ax = fig.add_subplot(111)
  #ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[xmin, xmax, ymin, ymax])
  #ax.plot(df.GEO_LAT, df.GEO_LONG, 'k.', markersize=2)
  #ax.set_xlim([xmin, xmax])
  #ax.set_ylim([ymin, ymax])
  #plt.show()
 
  centroid = {'lati':mlat, 'longi':mlon}
  print centroid['lati']
  jsonify(centroid=pd.DataFrame(centroid).to_dict())
  print centroid
  return render_template("output.html", 
                          cities= cities, 
                          cities2=cities2,
                          centroid=centroid,
                          weeks=weeks,
                          kdevalues=kdepos 

                          ) # 



