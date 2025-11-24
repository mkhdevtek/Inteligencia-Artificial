import cv2 as cv
import numpy as np
import os

print(cv.__version__)

dataset = './.training_images/people'
faces = os.listdir(dataset)
print(faces)

labels = []
facesData = []
label = 0

for face in faces:
    facePath = f'{dataset}/{face}'
    for faceName in os.listdir(facePath):
        img = cv.imread(f'{facePath}/{faceName}', 0)

        img = cv.resize(img, (30,30))

        facesData.append(img)
        labels.append(label)
        #print(f'Face: {faceName} in {facePath} appended to facesData')
    label += 1
    print(f'Label: {label}')

print(np.count_nonzero(np.array(labels) == 0))

print(f'len(facesData): {len(facesData)}')
print(f'len(labels): {len(labels)}')
print(f'Unique labels: {set(labels)}')


faceRecognizer = cv.face.EigenFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('./training_data/eigenface.xml')

