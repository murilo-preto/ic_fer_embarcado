import numpy as np
import os
import cv2 as cv
from rmn import RMN
import pandas as pd
from time import perf_counter

label_folder = 'val_set\\annotations'
image_folder = 'val_set\\images'

num2fex = {
    0 : 'neutral',
    1 : 'happy',
    2 : 'sad',
    3 : 'surprise',
    4 : 'fear',
    5 : 'disgust',
    6 : 'angry'
}

benchmark_df = pd.DataFrame(columns = ["Imagem", "FEX-esperada", "FEX-detectada", "Tempo" ])

def detect_fex(filepath):
    try:
        imagem_colorida = cv.imread(filepath)
        result = rmn.detect_emotion_for_single_face_image(imagem_colorida)
        fex = result[0]
        return fex              
    except Exception as e:
        print(e)
        return None

rmn = RMN()

img_and_fex = []
label_list = os.listdir(label_folder)
for label in label_list:
    prefix = (((label.split(sep="_"))[1]).split(sep="."))[0]
    if prefix == 'exp':
        num_fex = int(np.load(os.path.join(label_folder, label)))
        if num_fex in num2fex.keys():
            fex_esperada = num2fex[num_fex]
            img_and_fex.append([label.split('_')[0], fex_esperada])

img_and_fex.sort(key=lambda x:x[1])

all_images = os.listdir(image_folder)
numbered_item_list = [item.split(".")[0] for item in all_images]


for sublist in img_and_fex:
    file_num = sublist[0]
    fex_esperada = sublist[1]  

    if file_num in numbered_item_list:
        img_path = (os.path.join(image_folder, file_num)+'.jpg')
        tempo_inicial = perf_counter()
        fex_detectada = detect_fex(img_path)
        tempo = perf_counter()-tempo_inicial

        if fex_detectada != None:
            benchmark_df.loc[benchmark_df.shape[0]] = [file_num, fex_esperada, fex_detectada, tempo]
            print(file_num, fex_esperada, fex_detectada)

benchmark_df.to_csv(path_or_buf="fex.csv")