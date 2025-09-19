import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class MedicalImageLoader:
    def __init__(self, data_path):
        self.data_path = data_path
    
    def load_images(self, folder, target_size=(224, 224)):
        images = []
        labels = []
        path = os.path.join(self.data_path, folder)
        
        for class_name in os.listdir(path):
            class_path = os.path.join(path, class_name)
            if os.path.isdir(class_path):
                for img_name in os.listdir(class_path):
                    img_path = os.path.join(class_path, img_name)
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.resize(img, target_size)
                        images.append(img)
                        labels.append(class_name)
        
        return np.array(images), np.array(labels)
    
    def create_data_generator(self):
        return ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True
        )