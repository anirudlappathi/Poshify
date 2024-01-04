import cv2
import numpy as np

def get_limits(color):

    # write as np BGR color then convert using cv2
    BGRcolor = np.uint8([[color]])
    HSVcolor = cv2.cvtColor(BGRcolor, cv2.COLOR_BGR2HSV)

    lowerLimit = HSVcolor[0][0][0] - 10, 100, 100
    upperLimit = HSVcolor[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)

    return lowerLimit, upperLimit

