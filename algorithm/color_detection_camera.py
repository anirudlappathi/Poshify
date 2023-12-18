import cv2
import numpy as np
import base64

webcam = cv2.VideoCapture(0)

def process_image(image_data):
    print("process image time")
    base64_str = image_data.split(',')[1]
    img_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    HSVframe = HSVframe.reshape((-1, 3))
    HSVframe = np.float32(HSVframe)

    _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
    print("Dominant color:", dominant_color)

    return dominant_color.tolist()

def process_image(image_data):
    img_data = base64.b64decode(image_data)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Your OpenCV processing logic here to find dominant color
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    HSVframe = HSVframe.reshape((-1, 3))
    HSVframe = np.float32(HSVframe)

    _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
    print("Dominant color:", dominant_color)

    return dominant_color.tolist()

def detect_dominant_color_webcam():
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

if __name__ == "__main__":
    detect_dominant_color_webcam()