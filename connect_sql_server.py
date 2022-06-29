# %%
import configparser, urllib.parse

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
# %%

parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")

mssql_conf = parser["sqlserver"]
# %%
params = urllib.parse.quote_plus(
    f"DRIVER={mssql_conf['driver']};SERVER={mssql_conf['server']};DATABASE={mssql_conf['database']};UID={mssql_conf['uid']};PWD={mssql_conf['pwd']}")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
Base = declarative_base(bind = engine)

# %%
# https://stackoverflow.com/questions/57740618/prevent-sqlalchemy-from-automatically-setting-identity-insert
class Products(Base):
    __tablename__ = "Products"
    ProductID = Column(String, primary_key=True, autoincrement=False)
    ProductName = Column(String)
    Barcode = Column(String)

    def __init__(self,ProductID, ProductName, Barcode):
        self.ProductID = ProductID
        self.ProductName = ProductName
        self.Barcode = Barcode
        
    def __repr__(self):
        return "<Product %r>" % self.ProductID
