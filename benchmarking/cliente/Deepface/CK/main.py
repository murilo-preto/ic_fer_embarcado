import cv2 as cv
import os
import numpy as np
from time import perf_counter
from deepface import DeepFace

# Constants
IMAGE_DIR = "cohn-kanade-images"

# Initialize a list to hold results
results = [["name", "detectedFex", "time"]]

# Function to detect facial expression using DeepFace
def detect_facial_expression(filepath):
    try:
        image = cv.imread(filepath)
        result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False, silent=True)
        return result[0]['dominant_emotion']
    except Exception as e:
        print(e)
        return None

# Iterate through the directory and process images
for (root, _, files) in os.walk(IMAGE_DIR, topdown=False):
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    if 'Thumbs.db' in files:
        files.remove('Thumbs.db')

    if len(files) > 0:
        # Process the last 3 files and the first file in the directory
        selected_files = files[-3:] + [files[0]]

        for file in selected_files:
            image_path = os.path.join(root, file)
            initial_time = perf_counter()

            detected_expression = detect_facial_expression(image_path)

            if detected_expression is not None:
                processing_time = perf_counter() - initial_time
                results.append([file.strip(".png"), detected_expression, processing_time])
                print(image_path, detected_expression)

# Save the results to a CSV file
np.savetxt("benchmarkResult.csv", results, delimiter=",", fmt='%s')
