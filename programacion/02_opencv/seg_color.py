# Segmentación de color

import cv2 as cv

img = cv.imread('./content/bike.jpg', 1)
img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
ubb = (0, 60, 60) # umbral bajo 
uba = (10, 255, 255) # umbral alto
ubb1 = (170, 60, 60) # umbral bajo 
uba1 = (180, 255, 255) # umbral alto

# Los pixeles que cumplan los rangos (ubb, uba) extraen una maascara
mascara1 = cv.inRange(hsv, ubb, uba)
mascara2 = cv.inRange(hsv, ubb1, uba1)
mascara = mascara1 + mascara2
resultado = cv.bitwise_and(img, img, mask=mascara)

cv.imshow('img', img)
cv.imshow('img2', img2)
cv.imshow('hsv', hsv)
cv.imshow('mascara', mascara)
cv.imshow('resultado', resultado)

if cv.waitKey(0) & 0xFF == 27:
    exit(0)

cv.destroyAllWindows()
