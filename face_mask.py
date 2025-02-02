from imutils.video import VideoStream
from imutils import face_utils
import imutils
import time
import cv2
import dlib
from watermarking import watermarking

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\\opencv-face-master\opencv-face-master\shape_predictor_68_face_landmarks.dat")

print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)
glass = cv2.imread("D:\opencv-face-master\opencv-face-master\data\glass2.png", cv2.IMREAD_UNCHANGED)
moustache = cv2.imread("D:\opencv-face-master\opencv-face-master\data\moustache.png", cv2.IMREAD_UNCHANGED)


# loop over the frames from the video stream
while True:
    # grayscale
    frame = vs.read()
    frame = imutils.resize(frame, height=550)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     # detect faces in the grayayscale frame
    rects = detector(gray, 0)

    # loopop over found faces
    for rect in rects:
        shape = predictor(frame, rect)
        shape = face_utils.shape_to_np(shape)

        eyeLeftSide = 0
        eyeRightSide = 0
        eyeTopSide = 0
        eyeBottomSide = 0

        moustacheLeftSide = 0
        moustacheRightSide = 0
        moustacheTopSide = 0
        moustacheBottomSide = 0

        for (i, (x, y)) in enumerate(shape):
            if (i + 1) == 37:
                eyeLeftSide = x - 40
            if (i + 1) == 38:
                eyeTopSide = y - 30
            if (i + 1) == 46:
                eyeRightSide = x + 40
            if (i + 1) == 48:
                eyeBottomSide = y + 30

            if (i + 1) == 2:
                moustacheLeftSide = x
                moustacheTopSide = y - 10
            if (i + 1) == 16:
                moustacheRightSide = x
            if (i + 1) == 9:
                moustacheBottomSide = y

        eyesWidth= eyeRightSide - eyeLeftSide
        if eyesWidth < 0:
            eyesWidth = eyesWidth * -1

        # add glasses
        fitedGlass = imutils.resize(glass, width=eyesWidth)
        frame = watermarking(frame, fitedGlass, x= eyeLeftSide, y= eyeTopSide)


        moustacheWidth= moustacheRightSide - moustacheLeftSide
        if moustacheWidth < 0:
            moustacheWidth = moustacheWidth * -1
        # add moustache
        fitedMoustache = imutils.resize(moustache, width=moustacheWidth)
        frame = watermarking(frame, fitedMoustache, x= moustacheLeftSide, y= moustacheTopSide)

    # cv2.imshow("Glass", fitedGlass)
    key = cv2.waitKey(1) & 0xFF

     # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # show the frame
    cv2.imshow("Face Mask", frame)

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
