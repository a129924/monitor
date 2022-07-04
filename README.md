---
title: 監視器掃描輸入系統
---

# 監視器掃描輸入系統

## 目的

* 讓內勤可以快速地找到目前掃到的商品
* 減少人為上的疏失，大大減少時間的消耗

---
## 目標

### 這是什麼?
* 利用opencv讀取監視器的畫面，並且把掃描器所掃到的商品，透過API把詳細資料顯現在畫面上。

- [x] 可選擇多個監視器輸入。
- [x] 依照不同的掃描器，輸出到對應的畫面上。
- [x] 把結果儲存起來，讓內勤能夠快速找到問題。

### 使用情境
客人收到貨時，會有一些爭議，當時內勤是看監視器錄到的畫面，來找出問題的貨，所以公司想要有一個可以利用掃描器掃到的商品，來讓內勤可以快速地找到有問題的商品，減少找商品的時間，也能快速的看到目前掃到的商品。

---

## 執行環境
目前運行電腦版本為windows11
python環境為3.9.7，也使用了以下套件：

```txt=
aioflask==0.4.0
aiohttp==3.8.1
aiosignal==1.2.0
alphabet==0.0.8
asttokens==2.0.5
async-timeout==4.0.2
attrs==21.4.0
autopep8==1.6.0
backcall==0.2.0
certifi==2022.5.18.1
chardet==3.0.4
charset-normalizer==2.0.12
click==8.1.3
colorama==0.4.4
debugpy==1.6.0
decorator==5.1.1
entrypoints==0.4
et-xmlfile==1.1.0
executing==0.8.3
fake-useragent==0.1.11
filemagic==1.6
Flask==2.1.2
Flask-PyMongo==2.3.0
Flask-SQLAlchemy==2.5.1
frozenlist==1.3.0
googletrans==3.0.0
greenlet==1.1.2
greenletio==0.9.0
h11==0.9.0
h2==3.2.0
hpack==3.0.0
hstspreload==2021.12.1
httpcore==0.9.1
httpx==0.13.3
hyperframe==5.2.0
idna==2.10
importlib-metadata==4.11.4
ipykernel==6.15.0
ipython==8.4.0
itsdangerous==2.1.2
jedi==0.18.1
Jinja2==3.1.2
jsons==1.6.3
jupyter-client==7.3.4
jupyter-core==4.10.0
MarkupSafe==2.1.1
matplotlib-inline==0.1.3
multidict==6.0.2
nest-asyncio==1.5.5
numpy==1.22.4
opencv-python==4.6.0.66
openpyxl==3.0.10
packaging==21.3
pandas==1.4.2
parso==0.8.3
pickleshare==0.7.5
Pillow==9.1.1
prompt-toolkit==3.0.29
psutil==5.9.1
pure-eval==0.2.2
pycodestyle==2.8.0
Pygments==2.12.0
pymongo==4.1.1
pyodbc==4.0.32
pyparsing==3.0.9
python-dateutil==2.8.2
pytz==2022.1
pywin32==304
pyzmq==23.1.0
requests==2.28.0
rfc3986==1.5.0
six==1.16.0
sniffio==1.2.0
SQLAlchemy==1.4.37
stack-data==0.3.0
toml==0.10.2
tornado==6.1
traitlets==5.2.2.post1
typish==1.9.3
urllib3==1.26.9
uvicorn==0.18.2
wcwidth==0.2.5
Werkzeug==2.1.2
yarl==1.7.2
zipp==3.8.0

```

資料夾中有requirements.txt，可以利用pip install快速安裝所需要的套件
```shell=
$ pip install -r requirements.txt
```

---

## 如何使用

## 文件說明
在使用之前，我會依照功能性分成三個部份，一是API的輸入及輸出、二是監視器畫面的輸入輸出、三是資料庫的設定。
## (一) API輸入輸出
### API有兩大部份，Barcode機輸入條碼傳到API上以及API控制DB輸入輸出。
#### 第一部份，我先說明BARCODE輸入條碼的部分，負責的程式為`BarcodeInput.py`，程式碼如下：
```python=
#==========================BarcodeInput.py===================================
import requests

while True:
    product_id = input("input barcode: ")
    if product_id == "exit":
        break
    else:
        header = {"content-type": "application/json"}
        response = requests.patch(f"http://127.0.0.1:8081/API/MongoDB/PATCH/temp?device_id=1&product_id={product_id}",
                                headers=header, verify=False)

```
該程式是利用input，將條碼機掃到的資料，透過input傳送到API上，依照條件新增暫存資料，或者是更改暫存資料。

#### 第二部份，依照HIT到的API對DATABASE做輸入輸出，主要負責程式為`dbControl_API.py`。
在`dbControl_API.py`中有詳細的說明各個API的功能性，程式我擷取最重要的兩支API作呈現，程式碼如下。
```python=
#==========================dbControl_API.py===================================
from MSsql_Model import Products
from MongoDB_Model import mongo
from flask import jsonify, request
from ApiFormater import success_message, error_message, sqlalchemy_Products, mongo_Product
import asyncio
from aioflask import Flask

app = Flask(__name__)

app.config.from_object('FlaskSetting.config.DevelopmentConfig')

def the_mongo_value_exist(data)->bool:
    try:
        data[0]
        return True
    except IndexError:
        return False
    
# 最主要的兩支API其一 掃描器掃到的資料以及電腦的編號HIT到這支API 再依照條件做判斷
@app.route("/API/MongoDB/PATCH/temp", methods=["PATCH"])
def mongo_patch_temp():
    mydb = mongo.db
    # 抓取電腦編號及商品編號
    device_id, product_id = request.args.get('device_id'), request.args.get('product_id')
    # 設定條件
    filter_by = {"device_id":device_id}
    # 查詢
    temp_products = mydb.temp.find(filter_by)
    # 判斷是否有找尋到以及HIT到的商品編號是否相同
    if the_mongo_value_exist(temp_products) and temp_products[0]["ProductID"] == product_id: 
        temp_products = temp_products[0]
        del temp_products["_id"]
        # 直接回傳找尋到的資料
        return jsonify(success_message(result = temp_products)), 200
    else:
        try:
            product:dict[str:str] = mydb.Products.find({"ProductID":product_id})[0]
            del product['_id']
            # 判斷是否有找尋到以及HIT到的商品編號是否不同
            if the_mongo_value_exist(temp_products) and temp_products[0]["ProductID"] != product_id:
                # 做更動
                mydb.temp.update_one(filter_by,{"$set":product})
                # 回傳資料
                return jsonify(success_message(result = product)) ,200
            # 如果都沒有 新增資料
            else:
                insert_data = {
                    "device_id":device_id, 
                    'ProductID':product['ProductID'],
                    'ProductName':product['ProductName'],
                    "Barcode":product['Barcode']}
                mydb.temp.insert_one(insert_data)
                # 回傳資料
                return jsonify(success_message(result = insert_data)) ,200
        # 如果上述發生錯誤 會直接回傳404
        except Exception:
            return jsonify(error_message(code = 404)), 404
# 最主要的兩支API其二 監視器會依照電腦的編號 將資料HIT到這支API 再依照條件找尋符合的資料
@app.route("/API/MongoDB/GET/temp/<device_id>")
async def get_temp_product(device_id):
    mydb = mongo.db
    # 測試async的功能
    await asyncio.sleep(0.05)
    try:
        # 找尋相對應的電腦編號
        product = mydb.temp.find({"device_id":device_id})[0]
        del product['_id']
        # 回傳資料
        return jsonify(success_message(result = product)) ,200
    # 若發生錯誤 直接回傳404
    except Exception:
        return jsonify(error_message(code = 404)) ,404 
```
---  
## (二) 監視器畫面的輸入輸出。
### 主要負責程式為`loadVedio.py`
利用opencv讀取監視器的畫面，用Pillow在畫面上做把HIT到的資料，在畫面上做渲染，程式碼如下。
:bulb: **註記:** 程式碼目前的抓取範例影片，尚未接取單位監視器，但以實作筆電的攝影機當輸入畫面
```python=
#==========================loadVedio.py===================================
import cv2, datetime, requests, time
import numpy as np
from PIL import ImageFont, ImageDraw, Image

cap = cv2.VideoCapture(r".\Taiwan.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    # 取得影像寬度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 取得影像高度
fourcc = cv2.VideoWriter_fourcc(*'mp4v')        # 設定影片的格式為 MJPG
out = cv2.VideoWriter('Video/output.mp4', fourcc, 60.0, (width,  height))  # 產生空的影片

fontpath = r".\font\NotoSansCJKtc-DemiLight.otf"
font = ImageFont.truetype(fontpath, 45)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()
# 設定時間
set_time = datetime.datetime.now()
while cap.isOpened():
    # 重複設定時間
    now_time = datetime.datetime.now()
    # 控制API不要過多的HIT
    if (now_time >= set_time):
        req = requests.get("http://127.0.0.1:8081/API/MongoDB/GET/temp/1")
        # 設定0.5秒 HIT一次
        set_time = now_time + datetime.timedelta(seconds=0.5)
        # print(req)
    try:
        # 抓取API的資料
        product = req.json()["result"]
        result = f"\nProductName:{product['ProductName']}\nProductID:{product['ProductID']}"
    except Exception:
        product = None
        result = ""
        
    ret, frame = cap.read()             # 讀取影片的每一幀
    
    localtime = time.localtime()
    localtime = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)

    text = f"{localtime}{result}"
    
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    # 設定畫面
    imgPil = Image.fromarray(frame)
    # 設定畫畫的畫面
    draw = ImageDraw.Draw(imgPil)
    # 畫畫
    draw.text((20, 0), text, fill=(0,0,255), font=font)
    frame = np.array(imgPil)
    
    cv2.imshow('frame', frame)          # 如果讀取成功，顯示該幀的畫面
    out.write(frame)                    # 將取得的每一幀圖像寫入空的影片
    if cv2.waitKey(1) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break
cap.release()                           # 所有作業都完成後，釋放資源
cv2.destroyAllWindows() 
```

## (三) 資料庫的設定
目前公司資料庫是使用MSSQL，為了不讓MSSQL有過多的乘載，所以我在架設了一個MongoDB，做資料的存取。
設定DATABASE的程式有兩支，利用`flask_sqlalchemy`套件設定`MSSQL`的`MSsql_Model.py`，
程式碼如下:
```python=
#==========================MSsql_Model.py===================================
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import configparser, urllib.parse

parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")
mssql_conf = parser["sqlserver"]

params = urllib.parse.quote_plus(
    f"DRIVER={mssql_conf['driver']};SERVER={mssql_conf['server']};DATABASE={mssql_conf['database']};UID={mssql_conf['uid']};PWD={mssql_conf['pwd']}")

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db.init_app(app)

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
```
以及`flask_pymongo`套件設定`MongoDB`的`MongoDB_Model.py`。
```python=
#==========================MongoDB_Model.py===================================
from flask import Flask
from flask_pymongo import PyMongo

import configparser

parser = configparser.ConfigParser()
parser.read(r".\dbSetting\db.ini")
mongodb = parser["mongodb"]
print(mongodb["localhost"])

app = Flask(__name__)
param = (mongodb['localhost'], mongodb['db'])
app.config["MONGO_URI"] = "mongodb://localhost:%s/%s" % param
mongo = PyMongo(app)

```

利用這兩個套件讓管理DATABASE更加的輕鬆，也能讓其他人員看到時，能夠快速了解整理的架構。

## 附錄 @dataclass
另外我有用dataclass做API回傳格式的設定，讓後續的人可以知道格式長什麼樣子，該程式為`ApiFormater.py`，程式碼如下

```python=
#==========================ApiFormater.py===================================
from dataclasses import dataclass, field

@dataclass
class success_message:
    code:int=200
    message:str="Successed"
    status:bool=True
    result:dict[str:str]= field(default_factory=list)
    
@dataclass
class error_message: 
    code:int 
    message = "Successed"
    status:bool = False
    result:dict[str:str] = field(default_factory=list)
    
@dataclass
class sqlalchemy_Products:
    data:dict[str:str] = field(repr = False)
    ProductID:str = field(init=False)
    ProductName:str = field(init=False)
    Barcode:str = field(init=False)
    
    def __post_init__(self):
        self.ProductID = self.data["ProductID"]
        self.ProductName = self.data["ProductName"]
        self.Barcode = self.data["Barcode"]

@dataclass
class mongo_Product:
    data:list[dict] = field(repr = False)
    ProductID:str = field(init=False)
    ProductName:str = field(init=False)
    Barcode:str = field(init=False)
    
    def __post_init__(self):
        self.ProductID = self.data[0]["ProductID"]
        self.ProductName = self.data[0]["ProductName"]
        self.Barcode = self.data[0]["Barcode"]
```


---
###### tags: `python` `opencv` `API` `Flask` `SqlAlchemy` `Pymongo`
