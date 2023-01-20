import cv2 as cv
from rmn import RMN
import requests

print('Iniciando modelos')
opencv_path = "haarcascade_frontalface_default.xml"
opencv_modelo = cv.CascadeClassifier(opencv_path)
rmn = RMN()

print('Iniciando captura de imagem')
webcam = cv.VideoCapture(0)
webcam.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
webcam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 360)

while True:
    ret, imagem_colorida = webcam.read()
    imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)
    try:
        faces = opencv_modelo.detectMultiScale(
            imagem_cinza, scaleFactor=1.1, minNeighbors=4)
        for (x, y, w, h) in faces:  # Recortar imagens detectadas
            imagem_recortada = imagem_colorida[y:y+h, x:x+w]
            print('Face detectada')

            result = rmn.detect_emotion_for_single_face_image(imagem_recortada)

            r = requests.post(
                'http://localhost:3000/api/facialexpressions', json={"fex": result[0]})
            print(r.status_code)

    except Exception as e:
        print(e)
