import cv2
import numpy as np
import base64

def bgr_to_hsv(b, g, r):
    bgr_color = np.uint8([[[b, g, r]]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
    return hsv_color[0][0]

def adjust_brightness(frame, wanted_brightness):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(grayscale_frame)
    brightness_factor = wanted_brightness / mean[0]
    return cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)

def dominant_color_finder_dataurl(image_data):
    #f'data:image/jpeg;base64,{encoded_jpg}'
    # image data is just encoded_jpg
    img_data = base64.b64decode(image_data)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # frame = adjust_brightness(frame)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    # only capture the center 1/4 - 3/4
    h, w, _ = frame.shape
    h_start, h_end = h // 4, h // 4 * 3
    w_start, w_end = w // 4, w // 4 * 3
    cropped_frame = frame[h_start:h_end, w_start:w_end]
    HSVframe = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
    HSVframe = HSVframe.reshape((-1, 3))
    HSVframe = np.float32(HSVframe)
    _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
    dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0]
    return (int(dominant_color_hsv[0]) * 360) // 179, (int(dominant_color_hsv[1]) * 100) // 255, (int(dominant_color_hsv[2]) * 100) // 255

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
        if key == ord('p'):
            wanted_brightness += 5

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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def test_crop_image():
    pinkshirt = cv2.imread('static/clothing_images/4c96091e-7913-4892-bea3-551a86fb388c.jpeg')
    cv2.imshow("casd", pinkshirt)
    h, w, _ = pinkshirt.shape
    h_start, h_end = h // 4, h // 4 * 3
    w_start, w_end = w // 4, w // 4 * 3

    cropped_img = pinkshirt[h_start:h_end, w_start:w_end]
    cv2.imshow("cv2", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_crop_image()