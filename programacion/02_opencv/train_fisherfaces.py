import cv2 as cv
import numpy as np
import os

dataset = './training_images/emotions'
faces = os.listdir(dataset)
print(faces)

labels = []
facesData = []
label = 0

for face in faces:
    facePath = f'{dataset}/{face}'
    for faceName in os.listdir(facePath):
        labels.append(label)
        facesData.append(cv.imread(f'{facePath}/{faceName}', 0))
        print(f'Face: {faceName} in {facePath} appended to facesData')
    label = label + 1

print(np.count_nonzero(np.array(labels) == 0))

faceRecognizer = cv.face.FisherFaceRecognizer().create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('./training_data/fisherface.xml')

