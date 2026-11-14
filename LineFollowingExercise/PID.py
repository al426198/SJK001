import WebGUI
import HAL
import Frequency
import cv2

# standard linear velocity
V = 6.5

# error constants
Kp = 0.0055
Kd = 0.00025
Ki = 0.00000025

# previous error
prev_err = 0

# accumulated error
acc_err = 0

avg_err = 0
count = 0

while True:
    img = HAL.getImage()      # fetches image

    # mask image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))

    # find contours
    cont, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not cont:
        break                # car lost the line

    # calculate centroids
    M = cv2.moments(cont[0])
    cX, cY = 0, 0
    if M['m00'] != 0:
        cX, cY = M['m10'] / M['m00'], M['m01'] / M['m00']
    
    # calibrate turning speed
    # using the previous error
    # and the accumulated error
    if cX != 0:

        # proportional error
        err = img.shape[1]/2 - cX
        P = Kp * err

        # derivative error
        deriv_err = err - prev_err
        D = Kd * deriv_err

        # integral error
        acc_err += err
        I = Ki * acc_err

        HAL.setV(V)
        HAL.setW(P+D+I)

        # CMAE (cumulative moving average error)
        count += 1
        avg_err += err - avg_err/count
        if count % 100 == 0:
            print(f"CMAE at it. {count}: {avg_err}")

        # update error
        prev_err = err

    WebGUI.showImage(mask)