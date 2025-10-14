import cv2 as cv
import numpy as np

img = cv.imread('./content/colors.png', 1)
img = cv.resize(img, (400, 400))
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

ubb_g = (40, 100, 100) # umbral bajo 
uba_g = (80, 255, 255) # umbral alto

ubb_r1 = (0, 100, 20) # umbral bajo 
uba_r1 = (8, 255, 255) # umbral alto
ubb_r2 = (175, 100, 20) # umbral bajo 
uba_r2 = (179, 255, 255) # umbral alto

ubb_b = (100, 100, 100) # umbral bajo 
uba_b = (130, 255, 255) # umbral alto

ubb_y = (20, 100, 100) # umbral bajo 
uba_y = (35, 255, 255) # umbral alto

# Los pixeles que cumplan los rangos (ubb, uba) extraen una maascara
mascarag1 = cv.inRange(hsv, ubb_g, uba_g)
#mascarag1 = cv.bitwise_and(img, img, mask=mascarag1)
_,contornos_g = cv.findContours(mascarag1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for c in contornos_g:
    area = cv.contourArea(c)
    M = cv.moments(c)
    if (M["m00"]==0): M["m00"]=1
    x = int(M["m10"]/M["m00"])
    y = int(M['m01']/M['m00'])

    cv.circle(frame, (x,y), 7, (0,255,0), -1)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv.LINE_AA)
    nuevoContorno = cv.convexHull(c)
    cv.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)

mascara_r1 = cv.inRange(hsv, ubb_r1, uba_r1)
mascara_r2 = cv.inRange(hsv, ubb_r2, uba_r2)
mascara_r = mascara_r1 + mascara_r2
mascara_r = cv.bitwise_and(img, img, mask=mascara_r)

mascara_b = cv.inRange(hsv, ubb_b, uba_b)

mascara_y = cv.inRange(hsv, ubb_y, uba_y)

cv.imshow('img', img)
cv.imshow('hsv', hsv)
cv.imshow('mascara_verde', mascarag1)
cv.imshow('mascara_roja', mascara_r)
cv.imshow('mascara_azul', mascara_b)
cv.imshow('mascara_amarilla', mascara_y)

if cv.waitKey(0) & 0xFF == 27:
    exit(0)

cv.destroyAllWindows()
