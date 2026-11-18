import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os
import pickle

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'models', 'recommender_model.pkl')

# 2. IMAGE SETTINGS
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def train():
    print("🚀 Starting AI Training...")
    
    # 3. LOAD IMAGES
    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    # 4. BUILD MODEL (Simple CNN)
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(4, activation='softmax') # 4 Categories: Acc, Pant, Shoe, Top
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # 5. TRAIN
    if train_generator.samples > 0:
        model.fit(train_generator, epochs=5)
        
        # 6. SAVE MODEL (Using Pickle format as per your file structure)
        # Note: Usually we save as .h5, but for your structure we wrap it.
        print(f"💾 Saving model to {MODEL_SAVE_PATH}...")
        
        # We save the weights mostly, but here saving full Keras model inside pickle
        # Aana Keras model-a direct-a pickle panna mudiyadhu.
        # So namma '.h5' format use panradhu dhaan BEST.
        
        # CHANGE: Let's save as .h5 directly to be safe.
        h5_path = MODEL_SAVE_PATH.replace('.pkl', '.h5')
        model.save(h5_path)
        print("✅ Model Saved as .h5 (Standard Format)")
        print("⚠️ PLEASE UPDATE image_processing.py to load .h5 instead of .pkl")
        
    else:
        print("❌ No images found in dataset folder!")

if __name__ == '__main__':
    train()