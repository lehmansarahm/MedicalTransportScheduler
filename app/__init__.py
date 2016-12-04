from flask import Flask
import pymysql.cursors

# Connect to the database
#connection = pymysql.connect(host='10.109.133.147',
#							 port='3307',
#                             user='med',
#                             password='uber123',
#                             db='meduber',
#                             charset='utf8mb4',
#                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.config.from_object('config')

from app import views