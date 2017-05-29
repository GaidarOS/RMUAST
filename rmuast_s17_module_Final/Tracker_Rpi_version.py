#!/usr/bin/python

"""
Major inspiration for the code were guides from www.pyimagesearch.com
Installation guide for DroneKit http://python.dronekit.io/guide/quick_start.html#installation

send_ned_velocity function is taken from the "Guiding and Controlling Copter" section of DroneKit documentation
"""

# import the necessary packages
import cv2
import time
import numpy as np
from collections import deque
from picamera import PiCamera
# from os.path import expanduser
from pymavlink import mavutil
from picamera.array import PiRGBArray
from dronekit import connect, VehicleMode


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (61, 78, 60)
greenUpper = (135, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=32)
counter = 0
(dX, dY) = (0, 0)
direction = ""
combined = ""

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)  # (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640, 480))
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# home = expanduser("~")
# out = cv2.VideoWriter(home + '/output.avi', fourcc, 20.0, (640, 480))

# allow the camera to warmup
time.sleep(0.1)

# Initialize MAVLink connection parameters
connection_string = "/dev/ttyS0"
vehicle = connect(connection_string, baud=912600, wait_ready=True)
rndm = True


# Connect to the Vehicle.
while rndm:
    while not vehicle.mode.name == 'GUIDED':
        print("GUIDED MODE: OFF")
    else:
        print("GUIDED MODE: ON")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            frame = frame.array
            # grab the current frame

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

                # only proceed if the radius meets a minimum size
                if radius > 1:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)
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
                try:  # escape index errors when there are not enough frames in the queue
                    if counter >= 10 and i == 1 and pts[-10] is not None:
                        # compute the difference between the x and y
                        # coordinates and re-initialize the direction

                        try:  # escape type error when there is no conture and the center is of type None
                            (dX, dY) = center
                        except TypeError:
                            pass
                        dX -= (width / 2)
                        dY -= (height / 2)
                        (velX, velY) = ("0", "0")
                        # ensure there is significant movement in the
                        # x-direction
                        if abs(dX) > 5:
                            velX = 1 * dX if np.sign(dX) == 1 else -1 * abs(dX)
                            # ensure there is significant movement in the
                            # y-direction
                        if abs(dY) > 5:
                            velY = 1 * dY if np.sign(dY) == 1 else -1 * abs(dY)
                            # dirY = "North" if np.sign(dY) == 1 else "South"
                            # handle when both directions are non-empty
                        if velX != "" and velY != "":
                            combined = "{}:{}".format(velX, velY)
                            send_ned_velocity(velX, velY, 0, 0.04)
                            # otherwise, only one direction is non-empty
                        else:
                            combined = velX if velX != "" else velY
                            send_ned_velocity(velX, 0, 0, 0.04) if velX != "" else send_ned_velocity(0, velY, 0, 0.04)

                except IndexError:
                    pass

            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

            if vehicle.mode.name == "GUIDED":
                break

# Close vehicle object before exiting script
cv2.destroyAllWindows()
vehicle.close()

print("Completed")
