import cv2 as cv
import math

rostro = cv.CascadeClassifier('./training_data/haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture('./content/smile/Make People Smile Project (1080p_30fps_H264-128kbit_AAC).mp4')
i = 0

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in rostros:
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        frame2 = frame[y:y+h, x:x+w]

        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)

        if (i % 1 == 0):
            # write to the corresponding folder
            cv.imwrite(f'./.training_images/emotions/feli/{str(i)}.jpg', frame2)
            cv.imshow('rostros', frame2)

    cv.imshow('rostros', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 13 or k == 27 or k == 32:
        break

cap.release()
cv.destroyAllWindows()
