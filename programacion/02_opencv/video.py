import cv2 as cv

# ---------------------------
# video

#cap = cv.VideoCapture(0) # Toma el primer dispositivo de camara que encuentre
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
#cap.set(cv.CAP_PROP_FPS, 15)

cap = cv.VideoCapture('./content/cat.mp4')

count = 0
while True:
    res, img = cap.read()

#    if not res:
#        cap.set(cv.CAP_PROP_POS_FRAMES, 0) # loop the video
#        continue

#        cv.imwrite(f"./frames/frame{count}.jpg", img)     # save frame as JPEG file       
    count += 1

    cv.imshow('Fotograma', img)
    if cv.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()
