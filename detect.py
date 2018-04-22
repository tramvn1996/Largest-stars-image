import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
#ap.add_argument("-i","--image", required = True, help="rings.v3.skycell.1659.099.stk.i.unconv.fits.png")
args = vars(ap.parse_args())
#load the image
#image = cv2.imread(args["image"])
s="iiii"
st = "/home/tnguyen/BigData/project3/cinf401-project3/rings.v3.skycell.1322.015.stk.i.unconv.fits.png"
print(st)
image = cv2.imread(st ,0)
#image = cv2.imread('circle.jpg',0)
kernel = np.ones((5,5),np.uint8)
ero = cv2.erode(image, kernel, iterations = 1)
cv2.imwrite("Erosion.png" ,ero)
print("DONE")
output = ero.copy()
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(ero, cv2.HOUGH_GRADIENT, 1, 20,
              param1=30,
              param2=10,
              minRadius=10,
              maxRadius=100)
print("DONE2")
if circles is not None:
    circles = np.round(circles[0,:]).astype("int")
    print(circles)
    for (x,y,r) in circles:
        print(x)
        print(y)
        print(r)
        cv2.circle(output,(x,y),r,(0,255,0),4)
        cv2.rectangle(output, (x-5,y-5),(x+5,y+5),(0,128,255),-1)

    #cv2.imwrite("output", np.hstack([image,output]))
   # cv2.waitKey(0)

