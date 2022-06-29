# %%
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import configparser, urllib.parse
# %%
parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")
mssql_conf = parser["sqlserver"]

db = SQLAlchemy()
# %%
params = urllib.parse.quote_plus(
    f"DRIVER={mssql_conf['driver']};SERVER={mssql_conf['server']};DATABASE={mssql_conf['database']};UID={mssql_conf['uid']};PWD={mssql_conf['pwd']}")
# %%
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# %%
db = SQLAlchemy(app)
# %%
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db.init_app(app)

# %%
class Products(db.Model):
    __tablename__ = "Products"
    ProductID = db.Column(db.String, primary_key=True, autoincrement=False)
    ProductName = db.Column(db.String)
    Barcode = db.Column(db.String)
    
    def __init__(self, ProductID, ProductName, Barcode):
        self.ProductID = ProductID
        self.ProductName = ProductName
        self.Barcode = Barcode
        
    def __repr__(self):
        return "<Product %r>" % self.ProductID
    
    


# %%
