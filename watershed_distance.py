import cv2
import numpy as np

img = cv2.imread('water_coins.jpg',cv2.IMREAD_COLOR)


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

    #watershed
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #median_blur = cv2.medianBlur(gray_image,5)
    ret, thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


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

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)
    img[markers == -1] = [255,0,0]

    cv2.imshow('thresh',thresh)
    cv2.imshow('opening',opening)
    cv2.imshow('sure foreground',sure_fg)
    cv2.imshow('sure background',sure_bg)
    cv2.imshow('markers',markers)


    cv2.waitKey(100)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()

