import cv2
import os
import numpy as np

def load_and_preprocess_dataset(dataset_path):
    # Abstract-padi identified style, color, category analyze panna images-ah ready pannuvom
    data = []
    labels = []
    categories = ['tops', 'pants', 'shoes', 'accessories']
    
    for category in categories:
        path = os.path.join(dataset_path, category)
        label = categories.index(category)
        
        for img_name in os.listdir(path):
            try:
                img_path = os.path.join(path, img_name)
                # Image-ah load panni 224x224 (Standard AI size) resize pannuvom
                img = cv2.imread(img_path)
                img = cv2.resize(img, (224, 224))
                # Normalization (0-1 range) for deep learning accuracy
                data.append(img / 255.0)
                labels.append(label)
            except Exception as e:
                print(f"Error loading {img_name}: {e}")
                
    return np.array(data), np.array(labels)