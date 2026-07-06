import numpy as np
import cv2

img = cv2.imread('temp.jpg', 0)

if img is None:
    print("ERROR: temp.jpg not found.")
    exit(1)

kernel = np.ones((5, 5), np.uint8)

clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(7, 7))
cl1 = clahe.apply(img)

cl2 = cv2.medianBlur(cl1, 5)
th1 = cv2.adaptiveThreshold(
    cl2,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY_INV,
    25,
    3
)

blur = cv2.GaussianBlur(cl1, (5, 5), 0)
ret3, th3 = cv2.threshold(
    blur,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

th2 = th1 & th3

opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)

contours, hierarchy = cv2.findContours(
    opening,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_NONE
)

img1 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
dst = cv2.drawContours(img1, contours, -1, (0, 255, 0), 1)

cv2.imwrite("out.jpg", dst)
cv2.imwrite("dst.jpg", dst)