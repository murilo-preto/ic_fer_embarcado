import cv2 as cv
import dlib
import os
from rmn import RMN
import numpy as np
from time import perf_counter

image_dir = "CK+\extended-cohn-kanade-images\cohn-kanade-images"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"

rows = [["name", "fex", "time"]]

opencv_modelo = cv.CascadeClassifier(modelo_opencv) #Importa o modelo de detecção opencv
previsor_formato = dlib.shape_predictor(modelo_dlib) #Importa o previsor de formato dlib
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()

def detect_face(caminho_imagem):
    imagem_bruta = cv.imread(caminho_imagem)
    imagem_cinza = cv.cvtColor(imagem_bruta, cv.COLOR_BGR2GRAY)
    try:
        faces = opencv_modelo.detectMultiScale(
            imagem_cinza, scaleFactor=1.1, minNeighbors=4)
        for (x, y, w, h) in faces:  # Recortar imagens detectadas
            imagem_recortada = imagem_bruta[y:y+h, x:x+w]

            detectedFex = rmn.detect_emotion_for_single_face_image(imagem_recortada)
            return detectedFex[0]

    except Exception as e:
        print(e)
        return "null"

for (root,__,files) in os.walk(image_dir, topdown=False):
        if len(files)>0:
            if files == ['.DS_Store']:
                 continue
            else:
                if ('Thumbs.db' in files):
                    files.remove('Thumbs.db')
            
                for file in (files[-3:]):
                     imagePath = root + "\\" + file
                     initialTime = perf_counter()

                     fex = detect_face(imagePath)
                     print(imagePath, fex)

                     rows.append([file.strip(".png"), fex, (perf_counter()-initialTime)])

np.savetxt("benchmarkResult.csv",
        rows,
        delimiter =", ",
        fmt ='% s')