# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time


#attempt to add compability for ros
import sys
import roslib
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class image_converter:

	def __init__(self):
		# Publish to the MarkerLocator's original topic
		self.image_pub = rospy.Publisher("/markerlocator/image_raw",Image)
		# Subscribe from the Iris camera topic
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/iris/camera/image_raw",Image,self.callback)
		self.frame_gray=cv2.cvtColor()

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			type
		except CvBridgeError as e:
			print(e)

	# Display the image
	#cv2.imshow("Image window", cv_image)
	#cv2.waitKey(3)
		global frame_gray
		frame_gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame_gray, "8UC1"))
			print("published success")
		except CvBridgeError as e:
			print(e)





# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
				help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
				help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (0, 0, 128)#(85,41,71)
greenUpper = (179, 19, 161)#(118,66,105)


# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# if a video path was not supplied, grab the reference
## to the webcam


#image_sub = rospy.Subscriber("/markerlocator/image_raw",Image,imgConv.callback)
#camera = cv2.VideoCapture(image_sub)
#camera = image_sub



rospy.init_node('image_converter', anonymous=True)
ic = image_converter()

try:
	#rospy.spin()
	print("this is main running in class image converter")
except KeyboardInterrupt:
	print("Shutting down")

camera = ic.frame_gray
# Display the image
#cv2.imshow("Image window", cv_image)
#cv2.waitKey(3)
#camera =


#PID
def pid_controller(y, yc, h=1, Ti=1, Td=1, Kp=1, u0=0, e0=0):
	'''Calculate System Input using a PID Controller

	Arguments:
	y  .. Measured Output of the System
	yc .. Desired Output of the System
	h  .. Sampling Time
	Kp .. Controller Gain Constant
	Ti .. Controller Integration Constant
	Td .. Controller Derivation Constant
	u0 .. Initial state of the integrator
	e0 .. Initial error

	Make sure this function gets called every h seconds!
	'''
	# Step variable
	k = 0

	# Initialization
	ui_prev = u0
	e_prev = e0
	for _ in range(2):
		# Error between the desired and actual output
		e = yc - y
		print(e)
		# Integration Input
		if e !=0:
			ui = ui_prev + 1/Ti * h*e
			ud = 1/Td * (e - e_prev)/h
		else:
				ui = 0
				ud = 0

		# Adjust previous values
		e_prev = e
		ui_prev = ui

		# Calculate input for the system
		u = Kp * (e + ui + ud)

		k += 1
		print(u)
		yield u


# keep looping
while True:
	# grab the current frame
	#(grabbed, frame) = camera.read()
	frame= camera
	print type(frame)

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	height, width, channel=frame.shape

	#Calculate the camera center:
	framecenter=width/2,height/2

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

		# only proceed if the radius meets a minimum size
		if radius > 10:
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
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")

			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"

			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"

			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)

			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	#distance=framecenter-center
	try:
		ydistance=framecenter[1]-center[1]
		xdistance=framecenter[0]-center[0]
		cv2.putText(frame, "X: {}, Y: {}".format(xdistance, ydistance),
				(frame.shape[1]-110, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.35, (0, 0, 255), 1)


	except TypeError:
		pass

	#call PID
	try:
		u= pid_controller(xdistance,framecenter[0],1,1,1,20,0,1)
		#(y, yc, h=1, Ti=1, Td=1, Kp=1, u0=0, e0=0):
		#y=pid_controller(xdistance,framecenter[0],1,0,0,20,0,0)
		#u = y([])
		cv2.putText(frame, "PID X: {}, PID Y: {}".format(xdistance, ydistance),
				(frame.shape[1]-500, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 0, 0), 1)
		#print (u)

	except TypeError:
		pass


	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
				0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
				(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.35, (0, 0, 255), 1)
	cv2.putText(frame, "T: {}".format(time.time()),
			(frame.shape[1]-250, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
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
