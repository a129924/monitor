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

set_time = ""
now_time = ""
set_time = datetime.datetime.now()
while cap.isOpened():
    now_time = datetime.datetime.now()
    if (now_time >= set_time):
        req = requests.get("http://127.0.0.1:8081/API/MongoDB/GET/temp/1")
        set_time = now_time + datetime.timedelta(seconds=0.5)
        # print(req)
    try:
        product = req.json()["result"]
        result = f"\nProductName:{product['ProductName']}\nProductID:{product['ProductID']}"
    except Exception:
        product = None
        result = ""
        
    ret, frame = cap.read()             # 讀取影片的每一幀

    
    localtime = time.localtime()
    localtime = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)

    text = f"{localtime}{result}"
 
    # cv2.putText(frame,text,(40,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    
    imgPil = Image.fromarray(frame) 
    draw = ImageDraw.Draw(imgPil)
    
    draw.text((20, 0), text, fill=(0,0,255), font=font)
    frame = np.array(imgPil)
       
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # cv2.imshow('gray', gray)          # 顯示灰階影片
    cv2.imshow('frame', frame)          # 如果讀取成功，顯示該幀的畫面
    out.write(frame)                    # 將取得的每一幀圖像寫入空的影片
    if cv2.waitKey(1) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break
cap.release()                           # 所有作業都完成後，釋放資源
cv2.destroyAllWindows() 