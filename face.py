from imutils.video import VideoStream
from imutils import face_utils
import imutils
import argparse
import time
import cv2
import dlib

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\opencv-face-master\opencv-face-master\shape_predictor_68_face_landmarks.dat")

print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)

# glass = cv2.imread("data/glass.png")
# Load our overlay image: mustache.png
imgMustache = cv2.imread("D:\opencv-face-master\opencv-face-master\data\moustache.png",-1)

# Create the mask for the mustache
orig_mask = imgMustache[:,:,3]

# Create the inverted mask for the mustache
orig_mask_inv = cv2.bitwise_not(orig_mask)

# Convert mustache image to BGR
# and save the original image size (used later when re-sizing the image)
imgMustache = imgMustache[:,:,0:3]
origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]


# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read()
    frame = imutils.resize(frame, height=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     # detect faces in the grayayscale frame
    rects = detector(gray, 0)

    # loopop over the face detections
    for rect in rects:
        (x,y,w,h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

        shape = predictor(frame, rect)
        shape = face_utils.shape_to_np(shape)
        # Draw the face landmarks on the screen.
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw each of them
        for (i, (x, y)) in enumerate(shape):
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
            # cv2.putText(frame, str(i + 1), (x - 10, y - 10),
            #     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

    # show the frame
    cv2.imshow("Frame", frame)

    # added_image=cv2.add(frame, glass)
    # cv2.imshow("Frame 2", added_image)

    key = cv2.waitKey(1) & 0xFF

     # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
