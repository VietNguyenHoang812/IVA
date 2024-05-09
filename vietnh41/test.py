import cv2



video_path = "vietnh41/instrusion_example.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        cv2.imwrite("vietnh41/frame_base.jpg", frame)
        break