import cv2
import numpy as np
from ultralytics import YOLO
import time
from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors

from collections import defaultdict

track_history = defaultdict(lambda: [])
model = YOLO("yolov8s.pt")
names = model.model.names


video_path = "vietnh41/demo.avi"
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('vietnh41/instrusion_demo.mp4', fourcc, fps, (1280, 720), True)


while cap.isOpened():
    success, frame = cap.read()
    if success:
        frame = cv2.resize(frame, (1280, 720)) 
        cv2.imshow('Framee', frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# result.release()
cap.release()
out.release()
cv2.destroyAllWindows()


