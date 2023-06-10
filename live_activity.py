import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import *
from datetime import datetime
import os
import pyrebase
import firebase_admin
from firebase_admin import credentials, messaging


config = {
    "apiKey": "AIzaSyCpLrAt9s6VpBi_7V0kgf4oePgHmUPpxuM",
    "authDomain": "simon-79c64.firebaseapp.com",
    "databaseURL": "https://simon-79c64-default-rtdb.firebaseio.com",
    "projectId": "simon-79c64",
    "storageBucket": "simon-79c64.appspot.com",
    "messagingSenderId": "325606079924",
    "appId": "1:325606079924:web:e34c18a00a28e3fbf706e1",
    "measurementId": "G-G043NBSYC9",
    "serviceAccount": "serviceAccount.json"
}
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)


def sendPush(title, msg, registration_token, dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        tokens=registration_token,
    )

    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)


tokens = ["eUD4fde5RXGH0mBl8a-cA3:APA91bHBurx98ac4MF4d0UTLmM8RQEtmD5Bo1Q-_msg3tyblrP0MK-0yIAanhg8kdgDmUga4kaEnDTyEa8lubIQFfrdqxZXvB4wzofet-cCC2G8ubfd1PnSvDbT6h5NvGnvTKzRKA6X1"]
tokens1 = ["e81qA2xmS1CLYnoWX7SVYO:APA91bFSLjfHTxfknoVdUOXWII_J1eGOUfTxZEeFjDjpBvAF_Qx_mr2KjLmRj2wnuR-gTH7Vwhy7RbxDeQD6hoJU_dibqkjucglLYMsXHrMQ5Q2rxXH-WXfLuTf_734FmmUaI75GtJan"]

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

now = datetime.now()
current_time = int(now.strftime("%H"))
model = YOLO('yolov8n.pt')
# Menambahkan Fitur Titik Koordinat Menggunakan Mouse


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('Camera 1')
cv2.setMouseCallback('Camera 1', RGB)

cap = cv2.VideoCapture('rtsp://admin:Elektro123@192.168.0.100:554')


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
count = 0
tracker = Tracker()
area_c = set()
# Proses cetak gambar deteksi

if current_time >= 21 or current_time <= 5:
    def imgwrite(img):
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M")
        filename = '%s.png' % current_time
        cv2.imwrite(os.path.join(
            r".\img\channel1", filename), img)
        directory = "E:\Tugas_akhir\img\channel1\%s.png" % current_time
        sec_time = int(now.strftime("%S"))
        if sec_time < 5:
            storage.child('/image_cam1', filename).put(directory)
            sendPush("Detect Person Camera 1", filename, tokens)
            sendPush("Detect Person Camera 1", filename, tokens1)

    area1 = [(0, 0), (800, 0), (800, 400), (0, 400)]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 2 != 0:
            continue
        frame = cv2.resize(frame, (800, 400))
        results = model.predict(source=[frame], conf=0.45, save=False)
        total = len(results[0])
        for i in range(total):
            boxes = results[0].boxes
            a = results[0].boxes.boxes
            box = boxes[i]

            px = pd.DataFrame(a).astype("float")
            list = []
            conf = box.conf.numpy()[0]
            for index, row in px.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                c = class_list[d]
                if 'person' in c:
                    list.append([x1, y1, x2, y2])
                    cv2.putText(frame, str(c) + ' ' + str(round(conf, 2)), (x1, y1),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (x2, y2), 5, (255, 0, 255), -1)
                    hasil = cv2.pointPolygonTest(
                        np.array(area1, np.int32), ((x2, y2)),  False)

                    if hasil >= 0:
                        crop = frame[y1:y2, x1:x2]
                        imgwrite(crop)
                        cv2.imshow(str(id), crop)
                        area_c.add(id)

        cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255), 2)
        print(area_c)
        k = len(area_c)
        cv2.imshow("Camera 1", frame)
        cv2.putText(frame, str(k), (50, 80),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

        if cv2.waitKey(1) & 0xFF == 27:
            break

else:
    def imgwrite(img):
        now = datetime.now()
        current_time = now.strftime("%d_%m_%Y_%H_%M")
        sec_time = int(now.strftime("%S"))
        filename = '%s.png' % current_time
        cv2.imwrite(os.path.join(
            r".\img\channel1", filename), img)
        directory = "E:\Tugas_akhir\img\channel1\%s.png" % current_time
        storage.child('/image_cam1', filename).put(directory)
        sec_time = int(now.strftime("%S"))
        if sec_time < 5:
            storage.child('/image_cam1', filename).put(directory)
            sendPush("Detect Person Camera 1", filename, tokens)
            sendPush("Detect Person Camera 1", filename, tokens1)

    model1 = YOLO('best1.pt')
    
    # Uji coba tambak
    # area1 = [(298, 315), (316, 364), (378, 387), (709, 411),
    #         (1019, 393), (1019, 32), (835, 1), (369, 0)]
    #area1 = [(500,0), (400,424), (418,474), (459,497), (1019,497), (1019,0)]
    #area2 = [(0, 142), (217, 0), (0, 0)]
    #area2 = [(295,0), (0,211), (0,0)]
    # run
    # area1 = [(491, 34), (441, 402), (460, 469), (533, 499),
    #        (1019, 499), (1017, 22), (558, 30)]
    #area2 = [(344, 42), (0, 301), (0, 57), (218, 42)]
    # walk
    #area1 = [(371,0), (292,342), (319,426), (402,482), (694,490), (1017,473), (1019,33), (845,0) ]
    #area2 = [(0,180), (0,0), (202,0)]
    #squat and sit
    #area1 = [(523, 56), (616, 50), (848, 34), (1019, 33),
    #         (1019, 499), (543, 499), (482, 444)]
    area1 = [(206,354),(311,317),(471,359)]
    # malam_tambak1
    # area1 = [(159, 447), (265, 420), (630, 173), (623, 163), (585, 156),
    #         (401, 123), (142, 96), (0, 111), (0, 370), (107, 439)]
    #area2 = [(0,363), (0,93), (313,70), (381,78)]
    #area1 =  [(472,182), (479,252), (646,237), (628,176)]
    # secure_night
    #area1 =  [(516,239), (665,235), (661,180), (516,174)]
    # malam uji coba 2
    # security_siang
    # area1 = [(808, 223), (751, 218), (516, 217), (247, 220), (234, 222),
    #        (214, 225), (0, 252), (0, 499), (521, 499), (754, 312)]
    # area1 = [(360, 468), (460, 414), (499, 347), (251, 289), (10, 232),
    #         (0, 230), (0, 499), (241, 499)]
    # aktivitas
 #   area1 = [(594, 310), (598, 310), (552, 307), (333, 292), (22, 270),
 #            (0, 269), (0, 499), (289, 499)]
   # area1 = [(558, 305), (266, 263),
    #         (0, 229), (0, 499), (289, 499)]
  #  area1 = [(159, 447), (265, 420), (630, 173), (623, 163), (585, 156),
  #           (401, 123), (142, 96), (0, 111), (0, 370), (107, 439)]
    # area1 = [(270, 499), (645, 412), (1019, 260),
    #         (1019, 224), (724, 134), (515, 118), (464, 120), (288, 142), (0, 183), (129, 470)]
    #kamera_2
    #area1= [(427, 356), (587, 185), (391, 146), (203,128), (3, 132), (3,290), (90, 356)]

    #kamera1 multi-4 frame 640, 360
    #area1=[(145,157), (563, 353),(627, 350),(635, 282),(635, 115), (489, 113), (379, 116), (220,136)] 

    #kamera3 multi-4 frame 640,360
   # area1= [(85, 119), (322,95), (477, 91), (637, 119), (636, 310), (542, 357), (69,356)] 
    #kamera4 multi-4 frame 640, 360

    # Proses Deteksi Aktivitas dan Manusia
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 2 != 0:
            continue

        #frame = cv2.resize(frame, (1020, 500))
        frame = cv2.resize(frame, (640, 360))
        results1 = model1.predict(source=[frame], conf=0.45, save=False)
        total1 = len(results1[0])

        for i in range(total1):
            boxes = results1[0].boxes
            a = results1[0].boxes.boxes
            box = boxes[i]
            px = pd.DataFrame(a).astype("float")
            conf = box.conf.numpy()[0]

            for index, row in px.iterrows():
                # print(row)
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])
                d = int(row[5])
                if d == 0:
                    c = 'Run'
                    cv2.putText(frame, str(c), (x1, y2),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif d == 1:
                    c = 'Sit'
                    cv2.putText(frame, str(c), (x1, y2),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif d == 2:
                    c = 'squat'
                    cv2.putText(frame, str(c), (x1, y2),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                elif d == 3:
                    c = 'Walk'
                    cv2.putText(frame, str(c), (x1, y2),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)



        cv2.polylines(frame, [np.array(area1, np.int32)], True, (0, 0, 255), 2)
 #       cv2.polylines(frame, [np.array(area2, np.int32)], True, (0, 0, 255), 2)

        k = len(area_c)
        cv2.imshow("Camera 1", frame)
        cv2.putText(frame, str(k), (50, 80),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
