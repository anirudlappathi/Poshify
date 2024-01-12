import cv2
from PIL import Image
import pandas as pd
import numpy as np

import os
from segment_anything import SamPredictor, sam_model_registry
import cv2

def segment_image(cloth_filepath):
    image = cv2.imread(cloth_filepath)
    model_path = "algorithm/sam_vit_b_01ec64.pth"
    sam = sam_model_registry["vit_b"](checkpoint=model_path)
    predictor = SamPredictor(sam)
    h, w, _ = image.shape
    middle_h = h // 2
    middle_w = w // 2

    predictor.set_image(image)

    masks, scores, logits = predictor.predict(
        point_coords=np.asarray([[middle_h, middle_w]]),
        point_labels=np.asarray([1]),
        multimask_output=True
    )

    mask_channels, mask_height, mask_weight = masks.shape
    result_mask = np.zeros((mask_height, mask_weight), dtype=bool)

    for j in range(mask_channels):
        result_mask |= masks[j, :, :]

    result_mask = result_mask.astype(np.uint8)

    alpha_channel = np.ones(result_mask.shape, dtype=result_mask.dtype) * 255
    alpha_channel[result_mask == 0] = 0

    print(image.shape)
    print(alpha_channel.shape)
    print(image.dtype)
    print(alpha_channel.dtype)
    print(np.unique(alpha_channel))

    result_image = cv2.merge((image, alpha_channel))

    print(result_image.shape)

    cv2.imshow('with mask', result_image)
    cv2.imshow('mask', alpha_channel)
    cv2.waitKey(0)


def sift_classification(cloth_filepath):
    cloth = cv2.imread(cloth_filepath, cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(cloth, None) # none is mask
    return keypoints, descriptors
    
def append_sift_data(clothing_list, sift_csv):
    pass




if __name__ == "__main__":
    segment_image("static/clothing_images/1a8b6ce8-72ab-450a-88f8-11d8df3c036e.jpeg")