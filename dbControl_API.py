# %%
# %%
from MSsql_Model import Products
from MongoDB_Model import mongo
from flask import jsonify, request
from ApiFormater import success_message, error_message, sqlalchemy_Products, mongo_Product
import asyncio
from aioflask import Flask

app = Flask(__name__)

app.config.from_object('FlaskSetting.config.DevelopmentConfig')

def  the_mongo_value_exist(data)->bool:
    try:
        data[0]
        return True
    except IndexError:
        return False

@app.route("/API/MSSQL/GET", methods=["GET"])
@app.route("/API/MSSQL/GET/<product_id>", methods=["GET"])
def mssql_get_product(product_id:str):# V
    """MSSQL"""
    if product_id:
        query_barcode:dict[str] = Products.query.filter_by(ProductID=product_id).first().__dict__
        del query_barcode['_sa_instance_state']
        
        return jsonify(success_message(result = sqlalchemy_Products(query_barcode).data))
    else:
        query_datas = Products.query.all()
        data_list = [{"ProductID":query_data.ProductID, "ProductName":query_data.ProductName, "Barcode":query_data.Barcode} for query_data in query_datas]
        
        return jsonify(success_message(result = data_list))
    
@app.route("/API/POST/<product_id>", methods=["POST"])
def create_product(product_id):
    pass

@app.route("/API/MongoDB/GET/<product_id>", methods=["GET"])
def mongodb_get_product(product_id):
    """MongoDB"""
    
    product = mongo.db.Products.find({"ProductID":product_id})
    if  the_mongo_value_exist(product):
        result = mongo_Product(data = product).__dict__
        del result["data"]
        return jsonify(success_message(result = result))
    else:
        return jsonify(error_message(code = 404))
    

@app.route("/API/MongoDB/POST", methods=["POST"])
def mongo_new_product():
    data_list = request.json
    print(type(data_list))
    # mongo.db.Products.insert_many(data_list)
    response = jsonify(data_list)
    # response.headers["location"] = f"/API/MongoDB/{data[0]['username']}"
    return response

@app.route("/API/MongoDB/PATCH/temp", methods=["PATCH"])
def mongo_patch_temp():
    mydb = mongo.db
    device_id, product_id = request.args.get('device_id'), request.args.get('product_id')
    filter_by = {"device_id":device_id}
    temp_products = mydb.temp.find(filter_by)
    if the_mongo_value_exist(temp_products) and temp_products[0]["ProductID"] == product_id: 
        temp_products = temp_products[0]
        del temp_products["_id"]
        print(temp_products)
        return jsonify(success_message(result = temp_products))
    else:
        try:
            product:dict[str:str] = mydb.Products.find({"ProductID":product_id})[0]
            del product['_id']
            if the_mongo_value_exist(temp_products) and temp_products[0]["ProductID"] != product_id:
                mydb.temp.update_one(filter_by,{"$set":product})
                return jsonify(success_message(result = product)) ,200
            else:
                print("else")
                insert_data = {
                    "device_id":device_id, 
                    'ProductID':product['ProductID'],
                    'ProductName':product['ProductName'],
                    "Barcode":product['Barcode']}
                mydb.temp.insert_one(insert_data)
                
                return jsonify(success_message(result = insert_data)) ,200
        except Exception:
            return jsonify(error_message(code = 404)), 404
        
@app.route("/API/MongoDB/GET/temp/<device_id>")
async def get_temp_product(device_id):
    mydb = mongo.db
    await asyncio.sleep(0.01)
    try:
        product = mydb.temp.find({"device_id":device_id})[0]
        del product['_id']
        return jsonify(success_message(result = product)) ,200
    
    except Exception:
        return jsonify(error_message(code = 404)) ,404 

# =============================================
# %%
if __name__ == "__main__":
    app.run(port=8081)
    