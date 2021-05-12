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
cv2.createTrackbar("val4","Parameters",140,255,empty)
cv2.createTrackbar("val5","Parameters",255,255,empty)
cv2.createTrackbar("val6","Parameters",255,255,empty)

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
    val3 = cv2.getTrackbarPos("val3", "Parameters")
    val4 = cv2.getTrackbarPos("val4", "Parameters")
    val5 = cv2.getTrackbarPos("val5", "Parameters")
    val6 = cv2.getTrackbarPos("val6", "Parameters")

    #median_blur_color = cv2.medianBlur(img,5)
    #watershed
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median_blur = cv2.medianBlur(gray_image,5)
    ret, thresh = cv2.threshold(median_blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)





    low_blu = np.array([val1,val2,val3])
    high_blu = np.array([val4,val5,val6])

    #hsv = cv2.cvtColor(median_blur, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, low_blu, high_blu)
    #result = cv2.bitwise_and(img, img, mask = mask)
    
    thresh_mask = thresh
    watershed_blue = cv2.bitwise_and(img, img, mask = thresh_mask)

    #hsv2 = cv2.cvtColor(median_blur, cv2.COLOR_BGR2HSV)
    #mask2 = cv2.inRange(hsv2, low_blu, high_blu)
    #result2 = cv2.bitwise_and(watershed_blue, watershed_blue, mask = mask2)

    #getContours(mask2,imgContour)

    cv2.imshow('thresh',thresh)


    cv2.imshow('sure_fg',sure_fg)
    cv2.imshow('sure_bg',sure_bg)
    cv2.imshow('unknown',unknown)
    cv2.imshow('dist_transform',dist_transform)
    #cv2.imshow('watershed',watershed_blue)


    cv2.waitKey(100)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()

