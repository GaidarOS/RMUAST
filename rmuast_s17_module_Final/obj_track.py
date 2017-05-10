# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (105, 69, 113)
greenUpper = (154, 252, 247)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
combined = ""

# if a video path was not supplied, grab the reference
# to the webcam
camera = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, channels = frame.shape

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # print("center", center)  # contour center position in (width, height) format

        # if center[0] > width / 2:  # check if object is at the center of y axis
        #     if (width / 2) - center[0] > 5:
        #         print("need more speed left")
        #     elif (width / 2) - center[0] > 75:
        #         print("Give more speed")
        #     elif (width / 2) - center[0] > 150:
        #         print("Give moar speed")
        #     elif (width / 2) - center[0] > 250:
        #         print("Give much more speed")
        # else:
        #     if (width / 2) - center[0] < 5:
        #         print("need more speed right")
        #     elif (width / 2) - center[0] < 75:
        #         print("Give more speed right")
        #     elif (width / 2) - center[0] < 150:
        #         print("Give moar speed right")
        #     elif (width / 2) - center[0] < 250:
        #         print("Give much more speed right")# print((width / 2) - center[0])

        # if center[1] > height / 2:  # check if object is at the center of x axis
        #     print((height / 2) - center[1])

        # only proceed if the radius meets a minimum size
        if radius > 1:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue


        # check to see if enough points have been accumulated in
        # the buffer
        try:
            if counter >= 10 and i == 1 and pts[-10] is not None:
                # compute the difference between the x and y
                # coordinates and re-initialize the direction
                # text variables
                # dX = (pts[-10][0] - pts[i][0])
                # dY = (pts[-10][1] - pts[i][1])
                try:
                    (dX, dY) = center
                except TypeError:
                    pass
                dX -= (width / 2)
                dY -= (height / 2)
                (dirX, dirY) = ("", "")
                (velX, velY) = ("0", "0")
                # ensure there is significant movement in the
                # x-direction
                if abs(dX) > 5:
                    velX = 1 * dX if np.sign(dX) == 1 else -1 * abs(dX)
                    # dirX = "East" if np.sign(dX) == 1 else "West"

                # ensure there is significant movement in the
                # y-direction
                if abs(dY) > 5:
                    velY = 1 * dY if np.sign(dY) == 1 else -1 * abs(dY)
                    dirY = "North" if np.sign(dY) == 1 else "South"
                # handle when both directions are non-empty
                if velX != "" and velY != "":
                    combined = "{}:{}".format(velX, velY)
                    direction = "{}:{}".format(dirY, dirX)
                # otherwise, only one direction is non-empty
                else:
                    combined = velX if velX != "" else velY
                    direction = dirX if dirX != "" else dirY
        except IndexError:
            pass
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the movement deltas and the direction of movement on
    # the frame
    cv2.putText(frame, combined, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 0, 255), 3)
    cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

    # show the frame to our screen and increment the frame counter
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
