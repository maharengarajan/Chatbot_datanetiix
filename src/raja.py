from flask import Flask, jsonify, request
from datetime import datetime
import re
import requests
import mysql.connector as conn
from config import DATABASE_CONFIG
from logger import logger

app = Flask(__name__)

mydb = conn.connect(**DATABASE_CONFIG)
cursor = mydb.cursor()

current_date = datetime.now().date()
current_time = datetime.now().time()


    

    
if __name__ == '__main__':
    app.run()
