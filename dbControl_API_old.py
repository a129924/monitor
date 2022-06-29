# %%
# %%
from MSsql_Model import app, Products
from MongoDB_Model import mongo
from flask import jsonify, request
from dataclasses import dataclass
from ApiFormater import success_message, error_message, sqlalchemy_Products, mongo_Product, ID_Barcode

import asyncio

app.config.from_object('FlaskSetting.config.DevelopmentConfig')
def  the_mongo_value_exist(data)->bool:
    try:
        data[0]
        return True
    except IndexError:
        return False

@app.route("/API/MSSQL/GET", methods=["GET"])
@app.route("/API/MSSQL/GET/<barcode>", methods=["GET"])
def mssql_get_product(barcode:str):# V
    """MSSQL"""
    print(Products)
    if barcode:
        query_barcode:dict[str] = Products.query.filter_by(Barcode=barcode).first().__dict__
        del query_barcode['_sa_instance_state']
        
        return jsonify(success_message(result = sqlalchemy_Products(query_barcode).data))
    else:
        query_datas = Products.query.all()
        data_list = [{"ProductID":query_data.ProductID, "ProductName":query_data.ProductName, "Barcode":query_data.Barcode} for query_data in query_datas]
        
        return jsonify(success_message(result = data_list))
    
@app.route("/API/POST/<barcode>", methods=["POST"])
def create_product(barcode):
    pass

@app.route("/API/MongoDB/GET/<barcode>", methods=["GET"])
def mongodb_get_product(barcode):
    """MongoDB"""
    
    product = mongo.db.Products.find({"Barcode":barcode})
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
def mongo_get_temp():
    mydb = mongo.db
    device_id, barcode = request.args.get('device_id'), request.args.get('barcode')
    filter_by = {"device_id":device_id}
    temp_products = mydb.temp.find(filter_by)
    if the_mongo_value_exist(temp_products) and temp_products[0]["Barcode"] == barcode: 
        temp_products = temp_products[0]
        del temp_products["_id"]
        print(temp_products)
        return jsonify(success_message(result = temp_products))
    else:
        try:
            product:dict[str:str] = mydb.Products.find({"Barcode":barcode})[0]
            del product['_id']
            if the_mongo_value_exist(temp_products) and temp_products[0]["Barcode"] != barcode:
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

# =============================================

@app.route("/API/TEST")
async def return_results():
    
    id_filter = ID_Barcode(id = request.args.get('id'), barcode = request.args.get('barcode'))
    await asyncio.sleep(1)
    return jsonify(**id_filter.__dict__)

# %%
if __name__ == "__main__":
    app.run(port=8081)
    