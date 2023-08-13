import os
import pandas as pd

IMAGE_DIR = "datasets"

with open('dataEv.txt', 'w') as f:
    f.write('+-----+-----+-----+\n')

for (root, _, files) in os.walk(IMAGE_DIR, topdown=False):
    if files != []:
        for file in files:
            name = root.split("\\")[1]+"-"+root.split("\\")[2]+"-"+file.split(".")[0]
            print(name)

            csvPath = os.path.join(root,file)
            df = pd.read_csv(csvPath)
            median = df['time'].median()
            deviation = df['time'].std()
            print(f'{round(median,5)} +- {round(deviation,5)}')
            print('+-----+-----+-----+')

            with open('dataEv.txt', 'a') as f:
                f.write(f'{name}\n')
                f.write(f'{round(median,5)} +- {round(deviation,5)}\n')
                f.write('+-----+-----+-----+\n')