# # import numpy as np
# import cv2

# cv2.namedWindow("tracking")
# camera = cv2.VideoCapture(0)
# bbox = (638.0, 230.0, 56.0, 101.0)
# tracker = cv2.Tracker_create("KCF")
# init_once = False

# while camera.isOpened():
#     ok, image = camera.read()
#     if not ok:
#         print('no image read')
#         break

#     if not init_once:
#         ok = tracker.init(image, bbox)
#         init_once = True

#     ok, newbox = tracker.update(image)
#     print(ok, newbox)

#     if ok:
#         p1 = (int(newbox[0]), int(newbox[1]))
#         p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
#         cv2.rectangle(image, p1, p2, (200, 0, 0))

#     cv2.imshow("tracking", image)
#     k = cv2.waitKey(1) & 0xff
#     if k == 27:
#         break  # esc pressed

import cv2
import sys

if __name__ == '__main__':

    # Set up tracker.
    # Instead of MIL, you can also use
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN

    tracker = cv2.Tracker_create("MIL")

    # Read video
    video = cv2.VideoCapture(0)

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box
    bbox = (287, 23, 150, 150)

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255))

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
