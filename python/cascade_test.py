import numpy as np
import cv2

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#this is the cascade we just made. Call what you want
door_cascade = cv2.CascadeClassifier('75_75_100_230_5.xml')#'50_50_70_161.xml')

#cap = cv2.VideoCapture(0)
cam_width = 400

#pictures = [71, 81, 841, 114, 115, 681, 281, 101, 68]
pictures = [1,2,3,4,5]#,6,7,8,9,10]
for p in pictures:
    # Getting image from web-cam
    #ret, img = cap.read()
    img = cv2.imread('test/Anya/' + str(p) + '.jpg') # 5 84
    k = cam_width / img.shape[0]
    newx, newy = int(img.shape[1] * k), int(img.shape[0] * k)
    tmp_img = cv2.resize(img, (newx, newy))

    gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # cv.CascadeClassifier.detectMultiScale3(   image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize[, outputRejectLevels]]]]]]   )
    # image, reject levels level weights.
    doors = door_cascade.detectMultiScale(gray, 1.5, 50, 0, (int(tmp_img.shape[1] / 3), int(tmp_img.shape[0] / 3)), (tmp_img.shape[1], tmp_img.shape[0]))
    print(doors)
    #print(img.shape[0])
    #print(img.shape[1])
    #print(doors[0][1])
    # add this
    
    scale_coef = 600 / img.shape[0]
    newx, newy = int(img.shape[1] * scale_coef), int(600)
    img = cv2.resize(img, (newx, newy))
    for (x, y, w, h) in doors:
        obj_door = cv2.imread('dataset/good/8.bmp')
        newx, newy = int(w / k * scale_coef ), int(h / k * scale_coef )
        obj_door = cv2.resize(obj_door, (newx, newy))
        img[int(y / k * scale_coef):int(y / k * scale_coef) + obj_door.shape[0], int(x / k * scale_coef):int(x / k * scale_coef) + obj_door.shape[1]] = obj_door

    cv2.imshow('img', img)
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
        break;

#cap.release()
cv2.destroyAllWindows()