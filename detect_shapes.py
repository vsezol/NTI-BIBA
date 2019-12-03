"""Библиотеки"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

"""Функции"""

def detectShape(c):
    shape_id = -1
    shape_name = "unknown"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3:
        shape_name = "triangle"
        shape_id = 2
    elif len(approx) == 4:
        shape_name = "square"
        shape_id = 0
    elif len(approx) > 4:
        shape_name = "circle"
        shape_id = 1
    return shape_name, shape_id

def drawImage(inImg, w, h):
    fig, ax = plt.subplots()
    ax.imshow(inImg)
    fig.set_figwidth(w)
    fig.set_figheight(h)
    plt.show()

def drawGrid(img, step_x, step_y, bold):
  to_grid = img.copy()
  img_h, img_w = to_grid.shape[0], to_grid.shape[1]
  for x in range(0, img_w, step_x):
    cv2.line(to_grid, (x, 0), (x, img_h), (255,255,255), bold)
  for y in range(0, img_h, step_y):
    cv2.line(to_grid, (0, y), (img_w, y), (255,255,255), bold)
  return to_grid

"""Отсечка"""

t1 = cv2.getTickCount()

"""Считывание изображения"""

start_img = cv2.imread('/content/drive/My Drive/nti/img/n3.png')

"""Фильтрация"""

blured_img = cv2.GaussianBlur(start_img.copy(), (3, 3), cv2.BORDER_DEFAULT)

blured_img = cv2.bilateralFilter(blured_img, 20, 160, 50)
cv2.imwrite("/content/drive/My Drive/nti/output_img/blured_img.png", blured_img)

gray_img = cv2.cvtColor(blured_img, cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(gray_img, 100, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("/content/drive/My Drive/nti/output_img/thresh_img.png", thresh_img)

"""Поиск контуров"""

cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

"""Распознавание контуров"""

trigs = 0
circles = 0
squares = 0
shapes_array = [];
for c in cnts:
    try:
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape_name, shape_id = detectShape(c)
        if shape_id == 2:
            trigs += 1
        elif shape_id == 0:
            squares += 1
        elif shape_id == 1:
            circles += 1
        c = c.astype("int")
        cv2.drawContours(start_img, [c], -1, (0, 255, 0), 1)
        cv2.putText(start_img, shape_name, (cX, cY),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
        x = cX // 200
        y = cY // 200
        shapes_array.append(f'({shape_id}, {x}, {y})')
    except ZeroDivisionError:
        continue

"""Вывод"""

t2 = cv2.getTickCount()
all_t = (t2 - t1) / cv2.getTickFrequency()
start_img = drawGrid(start_img, 200, 200, 10)
drawImage(start_img, 7, 7)

print(f'Trigs: {trigs}\nSquares: {squares}\nCircles: {circles}')
print(f'Sum: {trigs + squares + circles}')
print('Time: ', all_t)

cv2.imwrite("/content/drive/My Drive/nti/output_img/output.png", start_img)

f = open('/content/drive/My Drive/nti/output_img/out.txt', 'w')
f.write('[' + ', '.join(shapes_array) + ']')
f.close()