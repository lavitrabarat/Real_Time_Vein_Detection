import cv2
import numpy as np
import time

def nothing(x):
    pass

def gstreamer_pipeline(capture_width=640, capture_height=480, framerate=32):
    return (
        "libcamerasrc ! "
        "video/x-raw, width=(int){}, height=(int){}, framerate=(fraction){}/1 ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true sync=false"
    ).format(capture_width, capture_height, framerate)

img1 = cv2.imread('out.jpg')

if img1 is None:
    print("ERROR: out.jpg not found.")
    exit(1)

cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("ERROR: Could not open camera via GStreamer/libcamera.")
    exit(1)

cv2.namedWindow('Vein Detection - Live Overlay')

time.sleep(0.5)

while True:
    ret, image = cap.read()

    if not ret or image is None:
        print("ERROR: Failed to grab frame.")
        break

    frame_h, frame_w = image.shape[:2]
    img1_resized = cv2.resize(img1, (frame_w, frame_h))

    dst = cv2.addWeighted(image, 0.7, img1_resized, 0.3, 0)

    cv2.imshow('Vein Detection - Live Overlay', dst)

    k = cv2.waitKey(1) & 0xFF

    if k == ord("a"):
        timestamp_filename = time.strftime("Vein_Screenshot%Y%m%d%H%M%S.jpg")
        cv2.imwrite(timestamp_filename, dst)
        break

    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()