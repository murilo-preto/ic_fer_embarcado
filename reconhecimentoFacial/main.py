import cv2 as cv
from rmn import RMN
import requests
import subprocess
import sys
import uuid

# MacAddress do servidor
serverMacAddress = "ff:ff:ff:ff:ff:ff"

# Obtem automaticamente MacAddress do dispositivo
localMacAddress = ":".join(["{:02x}".format(
    (uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1])
info_dict = {"macaddress": localMacAddress}

# Obtem IP local do servidor a partir do MacAddress
print(f'Tentando obter IP do servidor via ARP, usando MacAddress:{serverMacAddress}.\n')
cmd = f'arp -a | findstr "{serverMacAddress.replace(":", "-")}" '
try:
    returned_output = subprocess.check_output(
        cmd, shell=True, stderr=subprocess.STDOUT)
    parse = str(returned_output).split(' ', 1)
    serverIp = (parse[1].split(' '))[1]
    print(f"Utilizando IP local do servidor: {serverIp}.")
except Exception as e:
    print(
        f"Não foi possível obter o endereço de IP do servidor.\nErro:{e}\n")
    sys.exit(1)

# Inicia detecção
print('Iniciando modelos de detecção, pode demorar alguns minutos.')
opencv_path = "haarcascade_frontalface_default.xml"
opencv_modelo = cv.CascadeClassifier(opencv_path)
rmn = RMN()
webcam = cv.VideoCapture(0)

while True:
    ret, imagem_colorida = webcam.read()
    imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)
    try:
        faces = opencv_modelo.detectMultiScale(
            imagem_cinza, scaleFactor=1.1, minNeighbors=4)
        for (x, y, w, h) in faces:  # Recortar imagens detectadas
            imagem_recortada = imagem_colorida[y:y+h, x:x+w]
            print('Face detectada')

            detectedFex = rmn.detect_emotion_for_single_face_image(imagem_recortada)
            info_dict["fex"] = detectedFex[0]

            # Envia dados ao servidor
            r = requests.post(f'http://{serverIp}:3000/api/facialexpressions', json=info_dict)
            print(f"{info_dict} : {r.status_code}")

    except Exception as e:
        print(e)
