# %%
from flask import Flask
from flask_pymongo import PyMongo
# %%
import configparser
# %%
parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")
mongodb = parser["mongodb"]
print(mongodb["localhost"])
# %%
app = Flask(__name__)
param = (mongodb['localhost'], mongodb['db'])
app.config["MONGO_URI"] = "mongodb://localhost:%s/%s" % param
mongo = PyMongo(app)
# %%
# pipeline = [
#     {"$match": {"Barcode": 'Barcode1'}},
#     {"$lookup": {"from": 'temp', "localField": 'Barcode',
#                  "foreignField": 'Barcode', "as": 'Barcode'}}
# ]
