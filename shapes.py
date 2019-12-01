#!/usr/bin/env python3
import cv2
import imutils


trigs = 0
circles = 0
squares = 0


def detect(c):
    shapeName = "unknown shape"
    shapeID = -1
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3:
        shapeID = 2
        shapeName = "Triangle"
    elif len(approx) == 4:
        shapeID = 0
        shapeName = "Square"
    else:
        shapeID = 1
        shapeName = "Circle"
    return shapeName, shapeID


t1 = cv2.getTickCount()

start_img = cv2.imread('n3.png')
# resize = imutils.resize(start_img, width=start_img.shape[0]*2)
# ratio = start_img.shape[0] / float(resize.shape[0])

blured_img = cv2.GaussianBlur(start_img.copy(), (3, 3), cv2.BORDER_DEFAULT)
blured_img = cv2.bilateralFilter(blured_img, 20, 160, 50)
gray = cv2.cvtColor(blured_img, cv2.COLOR_BGR2GRAY)
#ТУТ ПОМЕНЯЙ.
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(
    thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    M = cv2.moments(c)
    # cX = int((M["m10"] / M["m00"]) * ratio)
    # cY = int((M["m01"] / M["m00"]) * ratio)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    name, sid = detect(c)

    if sid == 2:
        shapeID = 2
        trigs += 1
    elif sid == 0:
        shapeID = 0
        squares += 1
    elif sid == 1:
        shapeID = 0
        circles += 1

    # c = c.astype("float")
    # c *= ratio
    c = c.astype("int")
    cv2.drawContours(start_img, [c], -1, (0, 255, 0), 1)
    cv2.putText(
        start_img, name, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (255, 255, 255), 1)

# cv2.imshow("Image", start_img)
cv2.imwrite("output-n3.png", start_img)
cv2.waitKey(0)
print(
    "Trigs: {0}\nSquares: {1}\nCircles: {2}\n".format(
        trigs, squares, circles))
