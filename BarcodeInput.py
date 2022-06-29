import requests, json


while True:
    product_id = input("input barcode: ")
    if product_id == "exit":
        break
    else:
        header = {"content-type": "application/json"}
        response = requests.patch(f"http://127.0.0.1:8081/API/MongoDB/PATCH/temp?device_id=1&product_id={product_id}",
                                headers=header, verify=False)
        # print(json.loads(response.text)["result"])
