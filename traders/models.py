from django.db import models
from db_conn import db

# Create your models here.

trader_collection = db['traders']
trades = db['stocktrade']
