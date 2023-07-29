import os
import pandas as pd
import numpy as np

dfPath = "high-performance-desktop.csv"
mainFolder = "Emotion"

num2emotion = {
    "0": "neutral",
    "1": "angry",
    "2": "contempt",
    "3": "disgust",
    "4": "fear",
    "5": "happy",
    "6": "sad",
    "7": "surprise"
}

df = pd.read_csv(dfPath,skipinitialspace=True)

for emotionFolder, _, files in os.walk(mainFolder):
    if files != []:
        emotionTxtPath = os.path.join(emotionFolder,files[0])
        with open(emotionTxtPath) as f:
            lines = f.readlines()
            labelledEmotionNum = lines[0].strip()[0]
            
            if labelledEmotionNum != "2":
                labelledEmotion = num2emotion[labelledEmotionNum]
                imageName = files[0].strip("_emotion.txt").split("_")
                imageName = imageName[0]+"_"+imageName[1]

                df2 = df[df['name'].str.contains(imageName)]
                for index in df2.index:
                    df.loc[index, 'labelledFex'] = labelledEmotion

df2=df.dropna().reset_index(drop=True)
print(df2)

df2.to_csv('labelledHighPerformance.csv',index=False)
