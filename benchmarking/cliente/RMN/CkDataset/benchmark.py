import cv2 as cv
from os import walk
from rmn import RMN
import numpy as np
from time import perf_counter

image_dir = "cohn-kanade-images"
modelo_opencv = "haarcascade_frontalface_default.xml"

rows = [["name","detectedFex","time"]]

opencv_modelo = cv.CascadeClassifier(modelo_opencv)
rmn = RMN()

def detect_face(caminho_imagem):
    imagem_bruta = cv.imread(caminho_imagem)
    imagem_cinza = cv.cvtColor(imagem_bruta, cv.COLOR_BGR2GRAY)
    try:
        faces = opencv_modelo.detectMultiScale(
            imagem_cinza, scaleFactor=1.1, minNeighbors=4)
        for (x, y, w, h) in faces:
            imagem_recortada = imagem_bruta[y:y+h, x:x+w]

            detectedFex = rmn.detect_emotion_for_single_face_image(imagem_recortada)
            return detectedFex[0]

    except Exception as e:
        print(e)
        return "null"

for (root,__,files) in walk(image_dir, topdown=False):
        if len(files)>0:
            if files == ['.DS_Store']:
                continue
            else:
                if ('Thumbs.db' in files):
                    files.remove('Thumbs.db')

                tempList = files[-3:]
                tempList.insert(0,files[0])
            
                for file in (tempList):
                    imagePath = root + "\\" + file
                    initialTime = perf_counter()

                    fex = detect_face(imagePath)
                    rows.append([file.strip(".png"),fex,(perf_counter()-initialTime)])
                    
                    print(imagePath, fex)

np.savetxt("benchmarkResult.csv",
        rows,
        delimiter =",",
        fmt ='% s')
