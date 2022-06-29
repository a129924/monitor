# %%
from sre_constants import SUCCESS
import pandas as pd ,json
# %%
from connect_sql_server import Products, Session
# %%

class db_session:
    def __init__(self,dbSession, db_object):
        self.session = dbSession
        self.db_object = db_object
    
    def add_session(self,datas:dict)->str:
    
        try:
            self.session.add(self.db_object(**datas))
            self.session.commit()
        except Exception as e:
            print(e.__class__.__name__)
            print(str(e))
        finally:
            self.session.close()
            
        return "OK"
    
    def read_session(self,filter_params:dict)->json:
        result = self.session.query(self.db_object).filter_by(**filter_params).all()
        if result:
            return json.dumps({
                "code":200,
                "message":"Successed",
                "status":True,
                "result":{
                    "ProductID":result[0].ProductID,
                    "ProductName":result[0].ProductName,
                    "Barcode":result[0].Barcode,
                    }
            })
        else:
            return []
        
    
    def update_session(self):
        pass
    
    def delete_session(self):
        pass

# %%    
class excel_to_df:
    def __init__(self,filename:str):
        self._df = pd.read_excel(filename)
        
    def get_df(self)->pd.DataFrame:
        return self._df
    
    def setting_df(self,exchange_index:dict,filter:str)->pd.DataFrame:
        self._df.rename(columns=exchange_index, inplace=True)

        self._df.fillna(value=0, inplace=True)
        df_filter = self._df[self._df[filter] != 0]
        
        return df_filter

# %%
if __name__ == '__main__':
    filename = r".\file\20220620.xlsx"
    
    data = excel_to_df(filename)
    df:pd.DataFrame = data.get_df()
    
    original_index:list[str] = df.columns.values.tolist()
    replace_index:list[str] =  ["ProductID", "ProductName", "Barcode"] 
    
    exchange_index = dict(zip(original_index, replace_index))
    # %%
    df_filter = data.setting_df(exchange_index=exchange_index,filter="Barcode")
    max_row = len(df_filter)
    # %%
    MsSession = Session()
    db = db_session(MsSession, Products)
    # %%
    for index in range(max_row):
        datas = dict(zip(replace_index,df_filter.iloc[index].values.tolist()))
        db.add_session(datas)
        print(f"{datas} is commit")