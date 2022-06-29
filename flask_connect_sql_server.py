# %%
from dataclasses import dataclass
import configparser, urllib.parse

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.url import URL
# %%
parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")

mssql_conf = parser["sqlserver"]
db = SQLAlchemy()

# https://stackoverflow.com/questions/46739295/connect-to-mssql-database-using-flask-sqlalchemy
params = urllib.parse.quote_plus(
    f"DRIVER={mssql_conf['driver']};SERVER={mssql_conf['server']};DATABASE={mssql_conf['database']};UID={mssql_conf['uid']};PWD={mssql_conf['pwd']}")

app = Flask(__name__)
app.config.from_object('FlaskSetting.config.DevelopmentConfig')
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db.init_app(app)

@dataclass
class Products(db.Model):
    __tablename__ = "Products"
    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String)
    Barcode = Column(String)
    Price = Column(Integer)
    
@app.route('/create_db')
def index():
    print(params)

    db.create_all()
    return "create_db"  

@app.route('/select_table')
def select_table():
    sql_cmd = """
        select *
        from Products
        """
    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    
    return "select_table"

@app.route("/")
def Hello():
    return "Hello World!"

# %%

# f"DRIVER={mssql_conf['driver']};SERVER={mssql_conf['server']};DATABASE={mssql_conf['database']};UID={mssql_conf['uid']};PWD={mssql_conf['pwd']}"
# %%

# class Products(Base):
#     __tablename__ = "Products"
#     ProductID = Column(Integer, primary_key=True)
#     ProductName = Column(String)
#     Barcode = Column(String)
#     Price = Column(Integer)

if __name__ == '__main__':
    app.run(port=8081)
