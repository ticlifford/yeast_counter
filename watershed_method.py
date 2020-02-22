import cv2
import numpy as np

cap = cv2.VideoCapture(0)
img = cv2.imread('yeast.jpg',cv2.IMREAD_COLOR)
imgContour = img.copy()

def empty(a):
    pass

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(len(contours))
    areaMin = cv2.getTrackbarPos("area", "Parameters")
    print('areaMin:',areaMin,type(areaMin))
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("area", "Parameters")
#        print('area:',area)
        if area > areaMin:
            count += 1
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
#            print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
#            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)

    print('count:',count)
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("th1","Parameters",23,255,empty)
cv2.createTrackbar("th2","Parameters",20,255,empty)
cv2.createTrackbar("area","Parameters",200,500,empty)
#cv2.createTrackbar("Area","Parameters",5000,30000,empty)

while True:
    _, frame = cap.read()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (15,15), 0)
    kernel2 = np.ones((15,15), np.float32) /225
    blur_two = cv2.filter2D(gray_image,-1,kernel2)
    median_blur = cv2.medianBlur(gray_image,5)
    ret, thresh = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    getContours(thresh,imgContour)

    th1 = cv2.getTrackbarPos("th1", "Parameters")
    th2 = cv2.getTrackbarPos("th2", "Parameters")
    area = cv2.getTrackbarPos("area","Parameters")

    img_canny = cv2.Canny(median_blur,th1,th2)


    cv2.imshow('gray',gray_image)
    #thresh is best so far
    cv2.imshow('thresh',thresh)
    cv2.imshow('contour',imgContour)
    cv2.waitKey(500)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()

