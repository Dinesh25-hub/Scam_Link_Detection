# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import urllib.request
import urllib.parse
import scipy.ndimage as ndi
from skimage import transform
import seaborn as sns
import time
from datetime import datetime as dt

import csv
from browser_history.browsers import Firefox
from browser_history.browsers import Chrome

#sns.set_style('darkgrid')
#import plotly.express as px
from wordcloud import WordCloud
from scipy import signal
import scipy
#to supress warning
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')

import flask
from flask import Flask, render_template, request
# import joblib
# import sklearn.external.joblib as joblib
import joblib
import regex
import pickle
import sys
import logging
import tensorflow as tf
from feature import FeatureExtraction


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="phish_blocker"

)

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""
    
    return render_template('index.html',msg=msg)



@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('predict'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    msg=""

    
    if request.method=='POST':
        email=request.form['email']
        pwd=request.form['pass']
        cpwd=request.form['cpass']
        if pwd == cpwd :
            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM register WHERE email = %s ', (email,))
            account = cursor.fetchone()
            if account:
                session['email'] = email
                sql ="UPDATE register SET pass = %s WHERE email = %s"
                val = (pwd,email)
                cursor.execute(sql,val)
                mydb.commit()
                msg = 'Success'
                return redirect(url_for('login_user'))
            else:
                msg = 'Email Was Not Registered!'
        else:
            msg ="Password's Are Not Same"
            
    return render_template('forgot_password.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT count(*) FROM register where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql,val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
        
    return render_template('register.html',msg=msg)



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":

        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('predict.html',xx =round(y_pro_non_phishing,2),url=url )
    return render_template("predict.html", xx =-1)
    
        



@app.route('/history', methods=['GET', 'POST'])
def history():
    msg=""
    st=""
    data2=[]
    act=request.args.get("act")
    uname=""
    if 'username' in session:
        uname = session['username']

    ff=open("websites.txt","r")
    code=ff.read()
    ff.close()

    url=code.split(",")

    
    if request.method=='POST':
        
        name=request.form['name']
        if name=="Chrome":
            f = Chrome()
            outputs = f.fetch_history()
            his = outputs.histories
        elif name=="Firefox":
            f = Firefox()
            outputs = f.fetch_history()
            his = outputs.histories
        

        fieldnames = ['date', 'url_link']
        with open('static/data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(fieldnames)

            # write multiple rows
            writer.writerows(his)
        return redirect(url_for('history'))

    filename = 'static/data.csv'
    data1 = pd.read_csv(filename, header=0)
    st="1"

    for ss in data1.values:
        dt=[]
        dt.append(ss[0])
        dt.append(ss[1])
        data2.append(dt)

    return render_template('history.html',msg=msg,st=st,data2=data2)

@app.route('/url_block')
def url_block():
     if request.method == "POST":
        url = request.form["url"]
        Window_host = "C:\Windows\System32\drivers\etc\hosts"
        redirect1 = "127.0.0.1"
   
        while True:
         if (
                dt(dt.now().year, dt.now().month, dt.now().day, 1)
                < dt.now()
                < dt(dt.now().year, dt.now().month, dt.now().day, 24)
          ):
                with open(Window_host, "r+") as hostfile:
                 hosts = hostfile.read()
               
                 if url not in hosts:
                    hostfile.write(redirect1 + " " + url + "\n")    
         else:
            with open(Window_host, "r+") as hostfile:
                hosts = hostfile.readlines()
                hostfile.seek(0)
                for host in hosts:
                    if not any(url in host ):
                        hostfile.write(host)
                hostfile.truncate()
     return render_template("url_block.html")
      


##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


