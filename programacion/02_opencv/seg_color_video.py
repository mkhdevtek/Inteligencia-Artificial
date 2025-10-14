import cv2 as cv

cap = cv.VideoCapture(0)

ubb = (0, 100, 100)
uba = (10, 255, 255)

while True:
    ret, img = cap.read()
    cv.imshow('img', img)
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('gris', gris)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    cv.imshow('hsv', hsv)
    mascara = cv.inRange(hsv, ubb, uba)
    resultado = cv.bitwise_and(img, img, mask=mascara)

    cv.imshow('mascara', mascara)
    cv.imshow('resultado', resultado)

    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()

