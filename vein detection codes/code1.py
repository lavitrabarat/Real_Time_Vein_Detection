import cv2
import numpy as np
import time

def nothing(x):
    pass

def gstreamer_pipeline(capture_width=640, capture_height=480, framerate=32, flip_method=0):
    return (
        "libcamerasrc ! "
        "video/x-raw, width=(int){}, height=(int){}, framerate=(fraction){}/1 ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true sync=false"
    ).format(capture_width, capture_height, framerate)

cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("ERROR: Could not open camera via GStreamer/libcamera.")
    exit(1)

cv2.namedWindow('Vein Detection - CLAHE Preview')
cv2.createTrackbar('CLimit', 'Vein Detection - CLAHE Preview', 3, 8, nothing)

r = 2.0
time.sleep(0.5)

while True:
    ret, image = cap.read()

    if not ret or image is None:
        print("ERROR: Failed to grab frame from camera.")
        break

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=r, tileGridSize=(9, 9))
    cl1 = clahe.apply(gray)

    cv2.imshow('Vein Detection - CLAHE Preview', cl1)

    p = cv2.getTrackbarPos('CLimit', 'Vein Detection - CLAHE Preview')
    r = 0.5 + (p / 2)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('a'):
        timestamp_filename = time.strftime("Screenshot%Y%m%d%H%M%S.jpg")
        cv2.imwrite(timestamp_filename, cl1)
        cv2.imwrite("temp.jpg", cl1)
        break

    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()