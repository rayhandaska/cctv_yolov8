import cv2

pic_video = cv2.VideoCapture('kamera_3.mp4')

def VidFrame(waktu):
    pic_video.set(cv2.CAP_PROP_POS_MSEC, waktu*250)
    true_frames, image = pic_video.read()
    if true_frames:
        #menyimpan dalam bentuk file jpg
        cv2.imwrite("data/kamera3/kamera3_" + str(hitung)+".jpg", image)
    return true_frames 


waktu = 0
hitung = 1
berhasil = VidFrame(waktu)
while berhasil:
    hitung = hitung + 1
    waktu = waktu + 1
    waktu = round(waktu, 2)
    berhasil = VidFrame(waktu) 