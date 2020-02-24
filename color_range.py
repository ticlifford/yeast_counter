import cv2
import numpy as np

img = cv2.imread('yeast.jpg',cv2.IMREAD_COLOR)


def empty(a):
    pass
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("val1","Parameters",23,255,empty)
cv2.createTrackbar("val2","Parameters",20,255,empty)
cv2.createTrackbar("val3","Parameters",20,255,empty)
cv2.createTrackbar("area","Parameters",100,255,empty)

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    areaMin = cv2.getTrackbarPos("area", "Parameters")
    print('areaMin:',areaMin,type(areaMin))
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("area", "Parameters")

        if area > areaMin:

            count += 1
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(imgContour, (cX, cY), 2, (0, 0, 255), -1)
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)
        else:
            None
    print('count:',count)

while True:
    imgContour = img.copy()
    val1 = cv2.getTrackbarPos("val1", "Parameters")
    val2 = cv2.getTrackbarPos("val2", "Parameters")
    val3 = cv2.getTrackbarPos("val3","Parameters")
#    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    blurred_image = cv2.GaussianBlur(gray_image, (15,15), 0)
    blurred_image = cv2.GaussianBlur(img, (15,15), 0)
    kernel2 = np.ones((15,15), np.float32) /225
#    blur_two = cv2.filter2D(gray_image,-1,kernel2)
    median_blur = cv2.medianBlur(img,5)
    median_blur = cv2.medianBlur(median_blur,5)
#    ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    low_blu = np.array([val1,val2,val3])
    high_blu = np.array([130,255,255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low_blu, high_blu)
    result = cv2.bitwise_and(img, img, mask = mask)
    getContours(mask,imgContour)



    cv2.imshow('color',img)
#    cv2.imshow('thresh',thresh)
    cv2.imshow('median',median_blur)
    cv2.imshow('mask',mask)
    cv2.imshow('result',result)
    cv2.imshow('contours',imgContour)
    cv2.waitKey(500)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()

