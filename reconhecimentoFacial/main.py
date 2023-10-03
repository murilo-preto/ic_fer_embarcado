import cv2 as cv
from rmn import RMN
import requests
import subprocess
import sys
import uuid

# Server MAC Address
SERVER_MAC_ADDRESS = "ff:ff:ff:ff:ff:ff"

# Obtain the device's MAC Address automatically
local_mac_address = ":".join(["{:02x}".format(
    (uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1])
info_dict = {"macaddress": local_mac_address}

# Get the local server IP address from the MAC Address
if SERVER_MAC_ADDRESS != "ff:ff:ff:ff:ff:ff":
    print(f'Trying to obtain server IP via ARP, using MAC Address: {SERVER_MAC_ADDRESS}.\n')
    cmd = f'arp -a | findstr "{SERVER_MAC_ADDRESS.replace(":", "-")}" '
    try:
        returned_output = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT)
        parse = str(returned_output).split(' ', 1)
        server_ip = (parse[1].split(' '))[1]
        print(f"Using local server IP: {server_ip}.")
    except Exception as e:
        print(
            f"Unable to obtain the server's IP address.\nError: {e}\n")
        sys.exit(1)
else:
    print("Assuming server as localhost.")
    server_ip = 'localhost'

# Initialize detection models
print('Initializing detection models, this may take a few minutes.')
opencv_path = "haarcascade_frontalface_default.xml"
opencv_model = cv.CascadeClassifier(opencv_path)
rmn = RMN()
webcam = cv.VideoCapture(0)

while True:
    ret, color_image = webcam.read()
    gray_image = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
    try:
        # Detect faces
        faces = opencv_model.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=4)
        for (x, y, w, h) in faces:
            # Crop detected faces
            cropped_image = color_image[y:y+h, x:x+w]
            print('Face detected')

            # Detect emotion
            detected_emotion = rmn.detect_emotion_for_single_face_image(cropped_image)
            info_dict["fex"] = detected_emotion[0]

            # Send data to the server
            r = requests.post(f'http://{server_ip}:3000/api/facialexpressions', json=info_dict)
            print(f"{info_dict} : {r.status_code}")

    except Exception as e:
        print(e)
