from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv("labelled-standard-desktop.csv")

fex_esperada = df["labelledFex"]
fex_detectada = df["detectedFex"]

cf_matrix = confusion_matrix(fex_esperada, fex_detectada, labels=["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"])
cf_matrix_normalized = cf_matrix.astype('float') / cf_matrix.sum(axis=1)[:, np.newaxis]

print(cf_matrix_normalized)

fig, ax = plt.subplots(figsize=(7,7))

color = sns.cubehelix_palette(start=2.7, rot=0, dark=.02, light=.98, reverse=False, as_cmap=True)
ax = sns.heatmap(cf_matrix_normalized, annot=True, cmap=color, fmt='.2f', cbar=False, vmin=.05)

ax.set_title('Model: Residual Masking Network, dataset: CK+\n');
ax.set_xlabel('\nDetected Expressions')
ax.set_ylabel('Labelled Expressions\n');

ptbr_fex = ["Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise", "Neutral"]

ax.xaxis.set_ticklabels(ptbr_fex)
ax.yaxis.set_ticklabels(ptbr_fex)

plt.savefig('cmatrix-ck.png')