import cv2 as cv
import os

print(cv.__version__)

faceRecognizer = cv.face.EigenFaceRecognizer_create()
#faceRecognizer.read('./training_data/eliseo_EigenFace.xml')
faceRecognizer.read('./training_data/eigenface.xml')
print("archivo de entrenamiento cargado")

faces = ['eliseo', 'obed', 'pedro', 'sebas']
#faces = [ 'obed' ]

cap = cv.VideoCapture(0)

rostro = cv.CascadeClassifier('./training_data/haarcascade_frontalface_alt.xml')

while True:
    ret, frame = cap.read()
    if ret == False: break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cpGray = gray.copy()

    rostros = rostro.detectMultiScale(gray, 1.3, 3)

    for(x, y, w, h) in rostros:
        frame2 = cpGray[y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (30, 30), interpolation=cv.INTER_CUBIC)
        result = faceRecognizer.predict(frame2)
        #cv.putText(frame, '{}'.format(result), (x, y-20), 1, 3.3, (0, 0, 255), 1, 3)
        print(result[1])
        print(faces[result[0]])
        if result[1] > 800:
            cv.putText(frame, '{}'.format(faces[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv.LINE_AA)
            print(f'Rostro detectado: {faces[result[0]]}')
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        else:
            cv.putText(frame, 'DEsconocido', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv.LINE_AA)

            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv.imshow('frame', frame)
    k = cv.waitKey(1)
    if k == 13 or k == 27 or k == 32:
        break

cap.release()
cv.destroyAllWindows()
