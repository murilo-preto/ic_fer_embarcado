# Import necessary libraries
import numpy as np
import os
import pandas as pd
from time import perf_counter
from deepface import DeepFace
import cv2 as cv

# Define paths to annotation and image folders
annotation_folder = 'val_set\\annotations'
image_folder = 'val_set\\images'

# Mapping of numerical labels to facial expressions
expression_map = {
    0: 'neutral',
    1: 'happy',
    2: 'sad',
    3: 'surprise',
    4: 'fear',
    5: 'disgust',
    6: 'angry'
}

# Create an empty DataFrame to store benchmark results
benchmark_results_df = pd.DataFrame(columns=["image", "labelled_expression", "detected_expression", "processing_time"])

# Function to detect facial expression using DeepFace
def detect_facial_expression(filepath):
    try:
        image = cv.imread(filepath)
        result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False, silent=True)
        return result[0]['dominant_emotion']
    except Exception as e:
        print(e)
        return None

# Initialize list to hold image filenames and their corresponding labeled expressions
images_and_expressions = []

# Get list of annotation files
annotation_files = os.listdir(annotation_folder)

# Extract labeled facial expressions from annotation files
for annotation_filename in annotation_files:

    # Extract prefix from annotation filename
    expression_prefix = (((annotation_filename.split(sep="_"))[1]).split(sep="."))[0]

    # Check if prefix corresponds to labeled expression
    if expression_prefix == 'exp':

        # Load numerical expression label from annotation file
        expression_label = int(np.load(os.path.join(annotation_folder, annotation_filename)))

        # Check if the label is valid and map it to a facial expression
        if expression_label in expression_map.keys():
            labelled_expression = expression_map[expression_label]

            # Append image filename and labeled expression to the list
            images_and_expressions.append([annotation_filename.split('_')[0], labelled_expression])

# Sort the list based on the mapped expressions
images_and_expressions.sort(key=lambda x: x[1])

# Get list of all image filenames without extensions
all_image_filenames = os.listdir(image_folder)
numbered_image_list = [item.split(".")[0] for item in all_image_filenames]

# Iterate through the list of image filenames and labeled expressions
for image_expression_pair in images_and_expressions:
    image_num = image_expression_pair[0]
    labelled_expression = image_expression_pair[1]
    
    # Check if the image filename is in the list of images
    if image_num in numbered_image_list:

        # Construct full image path
        image_path = os.path.join(image_folder, image_num) + '.jpg'

        # Measure the initial time
        start_time = perf_counter()

        # Detect facial expression using the defined function
        detected_expression = detect_facial_expression(image_path)

        # Calculate elapsed time for processing
        processing_time = perf_counter() - start_time
        
        # Check if facial expression was detected
        if detected_expression is not None:
            
            # Add data to the benchmark DataFrame and print results
            benchmark_results_df.loc[benchmark_results_df.shape[0]] = [image_num, labelled_expression, detected_expression, processing_time]
            print(image_num, labelled_expression, detected_expression)

# Save benchmark data to a CSV file
benchmark_results_df.to_csv(path_or_buf="standard-desktop.csv", index=False)
