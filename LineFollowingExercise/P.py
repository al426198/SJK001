import WebGUI
import HAL
import Frequency
import cv2

# standard linear velocity
V = 4

# error constants
Kp = 0.005

while True:
    img = HAL.getImage()      # fetches image

    # mask image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))

    # find contours
    cont, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not cont:
        break                 # car lost the line

    # calculate centroids
    M = cv2.moments(cont[0])
    cX, cY = 0, 0
    if M['m00'] != 0:
        cX, cY = M['m10'] / M['m00'], M['m01'] / M['m00']

    # calibrate turning speed
    if cX != 0:

        # proportional error
        err = img.shape[1]/2 - cX
        P = err * Kp
        
        HAL.setV(V)
        HAL.setW(P)

    WebGUI.showImage(mask)
 