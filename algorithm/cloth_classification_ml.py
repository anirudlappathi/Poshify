import cv2
from PIL import Image
import pandas as pd

import os
from segment_anything import SamPredictor, sam_model_registry
import cv2

def segment_image(cloth_filepath):
    image = cv2.imread()
    model_path = "./sam_vit_b_01ec64.pth"
    sam = sam_model_registry["vit_b"](checkpoint=model_path)
    predictor = SamPredictor(sam)



    cloth = cv2.imread(cloth_filepath, cv2.IMREAD_UNCHANGED)


def sift_classification(cloth_filepath):
    cloth = cv2.imread(cloth_filepath, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(cloth, None) # none is mask
    return keypoints, descriptors
    
def append_sift_data(clothing_list, sift_csv):




if __name__ == "__main__":
    sift_classification_test()