#xác định vị trí khuôn mặt trong khung hình
# thư viện imitils hỗ trợ xử lý thay đổi kích thước khung hình
# dlib dùng phát hiện khuôn mặt với mô hình hog

from imutils.video import VideoStream
from imutils import face_utils
import imutils
import argparse
import time
import cv2
import dlib

print("[INFO] loadinig facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
#Hàm phát hiện khuôn mặt được cung cấp bởi Dlib Sử dụng mô hình HOG để phát hiện khuôn mặt trong ảnh.
print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start() #Khởi động camera mặc định của hệ thống (0 là ID mặc định).
time.sleep(2.0) #Tạm dừng 2 giây để camera ổn định trước khi xử lý.

# Vòng lặp xử lý video
while True:
    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    frame = vs.read() #Lấy khung hình tiếp theo từ webcam.
    frame = imutils.resize(frame, height=600) #Điều chỉnh kích thước khung hình, đặt chiều cao là 600 pixel để giảm kích thước xử lý.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Chuyển đổi khung hình từ ảnh màu (BGR) sang ảnh xám (grayscale) để tối ưu phát hiện khuôn mặt.
     # detect faces in the grayayscale frame
    rects = detector(gray, 0) #gray: Ảnh đầu vào,Tham số điều chỉnh độ chính xác (0 là mức mặc định).

    # Vẽ khung chữ nhật quanh khuôn mặt
    for rect in rects:
        (x,y,w,h) = face_utils.rect_to_bb(rect) #Chuyển đổi tọa độ của đối tượng rect (trả về bởi Dlib) thành định dạng (x, y, w, h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255, 0), 1)

    #  Hiển thị khung hình hiện tại với tên cửa sổ là "Frame"
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

     # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
