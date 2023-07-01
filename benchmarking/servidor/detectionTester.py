import uuid
from random import randrange, randint, choice
from time import sleep
import requests

# Config
simulationInterval = 0.5
numberOfSimulation = 100
serverIp = "192.168.0.8:3000"
numberOfMac = 25

# Busca e formata endereco macadress do dispositivo
# localMacAddress = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1])

def macGenerator(numberOfMac):
    for i in range(numberOfMac):
        newAddress = "%02x:%02x:%02x:%02x:%02x:%02x" % (
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            randint(0, 255),
            randint(0, 255)
            )
        macAddList.append(newAddress)

# Lista de fex para sortear
fexList = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
macAddList = []

macGenerator(numberOfMac)

# Simula usuario enviando macaddress e fex
for i in range(numberOfSimulation):
    simulatedFex = fexList[randrange(len(fexList))]
    sleep(simulationInterval)

    info_dict = {"macaddress": choice(macAddList), "fex": simulatedFex}

    try:
        r = requests.post(f'http://{serverIp}/api/facialexpressions', json=info_dict)
        print(f"{i} - {info_dict} : {r.status_code}")
    except Exception as e:
        print(e)
