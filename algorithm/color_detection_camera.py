import cv2
import numpy as np
import base64
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt
import urllib.request
import os


def bgr_to_hsv(b, g, r):
    bgr_color = np.uint8([[[b, g, r]]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

def adjust_brightness(frame, wanted_brightness):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(grayscale_frame)
    brightness_factor = wanted_brightness / mean[0]
    return cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)

# but in a decoded base64 image
def segment_cloth(img_bytes):
    model_path = './sam_vit_b_01ec64.pth'
    url = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth'

    if not os.path.exists(model_path):
        urllib.request.urlretrieve(url, model_path)
    sam = sam_model_registry["vit_b"](checkpoint=model_path)
    predictor = SamPredictor(sam)
    cv2image = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

    height, width, _ = cv2image.shape
    x = width // 2
    y = height // 2
    predictor.set_image(cv2image)
    masks, _, _ = predictor.predict(
                                    point_coords=np.asarray([[x, y]]),
                                    point_labels=np.asarray([1]),
                                    multimask_output=True
                                )
    C, H, W = masks.shape
    result_mask = np.zeros((H, W), dtype=bool)
    for j in range(C):
        result_mask |= masks[j, :, :]
    result_mask = result_mask.astype(np.uint8)
    print('result_mask', result_mask)

    alpha_channel = np.ones(result_mask.shape, dtype=np.uint8) * 255
    alpha_channel[result_mask == 0] = 0

    # Convert the alpha channel into an image
    alpha_image = cv2.cvtColor(alpha_channel, cv2.COLOR_GRAY2BGR)

    # Save the alpha channel image as a JPEG file
    alpha_bytes = cv2.imencode('.jpg', alpha_image)[1]
    with open('test_mask_output.jpg', 'wb') as file:
        file.write(alpha_bytes)

    # # Invert alpha_channel to use it as a mask
    # inverted_alpha = cv2.bitwise_not(alpha_channel)

    # Create a white background image
    result_image = cv2.merge((alpha_bytes, cv2image))

    white_background = np.ones(cv2image.shape, dtype=np.uint8) * 255

    # Mask the white background with the inverted alpha channel
    masked_background = cv2.bitwise_and(white_background, white_background, mask=alpha_channel)

    # Combine the masked background with the alpha image and get the final image
    result_image = cv2.merge((masked_background, alpha_image))

    # Save the resulting image as a JPEG file
    selection_bytes = cv2.imencode('.jpg', result_image)[1]
    with open('test_output.jpg', 'wb') as file:
        file.write(selection_bytes)
    # selection_image = cv2.merge((cv2image, alpha_channel))
    # selection_bytes = cv2.imencode('.jpg', selection_image)[1]
    # with open('test_output.jpg', 'wb') as file:
    #     file.write(selection_bytes)

    return selection_bytes.tobytes()

def dominant_color_finder_dataurl(image_data, filename):
    try:
        #f'data:image/jpeg;base64,{encoded_jpg}'
        # image data is just encoded_jpg
        img_bytes = base64.b64decode(image_data)
        
        # img_bytes = segment_cloth(img_bytes)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = adjust_brightness(cv2.imdecode(nparr, cv2.IMREAD_COLOR), 200)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 5
        HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        HSVframe = HSVframe.reshape((-1, 3))
        HSVframe = np.float32(HSVframe)

        _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
        dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0]
        print('a',dominant_color_hsv)
        # 360 100 100
        return (int(dominant_color_hsv[0]) * 360) // 179, (int(dominant_color_hsv[1]) * 100) // 255, (int(dominant_color_hsv[2]) * 100) // 255
    except Exception as e:
        os.remove(filename)

def detect_dominant_color_webcam():
    webcam = cv2.VideoCapture(0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    time = 0
    while True:
        _, frame = webcam.read()
        if time % 100 == 0:
            HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            HSVframe = HSVframe.reshape((-1, 3))
            HSVframe = np.float32(HSVframe)

            _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
            print(dominant_color)
            time = 0
        cv2.imshow("frame", frame)
        time += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
        
def create_contours_webcam():
    webcam = cv2.VideoCapture(0)
    object_detector = cv2.createBackgroundSubtractorMOG2()
    while True:

        _, frame = webcam.read()
        mask = object_detector.apply(frame)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #print(heirarchy)
        for i in contours:
            if cv2.contourArea(i) > 5000:
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                #cv2.drawContours(frame, [i], -1, (0, 255, 0), 3)

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()

def brighten_webcam():

    webcam = cv2.VideoCapture(0)

    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 30    # Brightness control (0-100)
    wanted_brightness = 150
    while True:
        _, frame = webcam.read()

        adjusted_image = adjust_brightness(frame, wanted_brightness)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('o'):
            wanted_brightness -= 5
            print(wanted_brightness)
        if key == ord('p'):
            wanted_brightness += 5
            print(wanted_brightness)

        cv2.imshow('Adjusted Image', adjusted_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def testing_brightness():

    webcam = cv2.VideoCapture(0)
    while True:
        _, frame = webcam.read()
        frame = adjust_brightness(frame, 200)
        cv2.imshow('frame', frame)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 5
        HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        HSVframe = HSVframe.reshape((-1, 3))
        HSVframe = np.float32(HSVframe)

        _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
        dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0]
        print('a',dominant_color_hsv)
        print(dominant_color_hsv[0])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testing_brightness()