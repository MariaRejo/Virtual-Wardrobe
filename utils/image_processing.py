import tensorflow as tf
import numpy as np
import cv2
import os

# 1. SETUP PATHS
BASE_DIR = os.getcwd()

# 👇 MUKKIYAM: .pkl illa, .h5 nu irukkanum!
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'recommender_model.h5')

ai_model = None

def load_model():
    global ai_model
    if ai_model is None:
        try:
            print(f"🔄 Loading AI Brain from: {MODEL_PATH}")
            
            # Check if file exists
            if not os.path.exists(MODEL_PATH):
                print(f"❌ Model file NOT FOUND at {MODEL_PATH}")
                print("⚠️ Please run 'python training/train_model.py' first.")
                return None

            # 👇 Loading the .h5 Model (Correct Way)
            ai_model = tf.keras.models.load_model(MODEL_PATH)
            print("✅ AI Brain Loaded Successfully!")
            
        except Exception as e:
            print(f"❌ Error Loading Model: {e}")
            return None
    return ai_model

def get_dominant_color(image):
    try:
        height, width, _ = image.shape
        # Crop center
        start_row, start_col = int(height * 0.25), int(width * 0.25)
        end_row, end_col = int(height * 0.75), int(width * 0.75)
        cropped_img = image[start_row:end_row, start_col:end_col]
        
        # Average color
        avg_color_per_row = np.average(cropped_img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        b, g, r = avg_color
        
        # Color Logic
        if r > 200 and g > 200 and b > 200: return "White"
        if r < 60 and g < 60 and b < 60:    return "Black"
        if r > 150 and g > 150 and b < 100: return "Yellow"
        if r > 100 and g > 100 and b > 100: return "Grey"
        if r > g and r > b: return "Red"
        if b > r and b > g: return "Blue"
        if g > r and g > b: return "Green"
        
        return "Multi-Color"
    except:
        return "Multi"

def analyze_image(image_path):
    model = load_model()
    
    if model is None:
        return "Unknown", "Unknown"

    try:
        img = cv2.imread(image_path)
        if img is None: return "Error", "Error"

        img_resized = cv2.resize(img, (224, 224)) 
        img_normalized = img_resized / 255.0
        img_batch = np.expand_dims(img_normalized, axis=0)

        predictions = model.predict(img_batch)
        class_index = np.argmax(predictions)
        
        # Alphabetical Order: 0-Accessory, 1-Pant, 2-Shoe, 3-Top
        categories = ['Accessory', 'Pant', 'Shoe', 'Top'] 
        
        if class_index < len(categories):
            detected_category = categories[class_index]
        else:
            detected_category = "Unknown"

        detected_color = get_dominant_color(img)
        
        return detected_category, detected_color

    except Exception as e:
        print(f"❌ Analysis Logic Error: {e}")
        return "Error", "Error"