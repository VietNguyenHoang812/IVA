import cv2
import numpy as np
import time

from collections import defaultdict
from ultralytics import YOLO
from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors


track_history = defaultdict(lambda: [])
model = YOLO("yolov8s.pt")
names = model.model.names


video_path = "vietnh41/instrusion_example.mp4"
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"

w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

output = 'vietnh41/demo.avi'
codec = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output, codec, fps, (w, h))

prev_frame_time = 0
new_frame_time = 0
down = {}
counter_down = set()

top_left  = (1094, 319)
top_right = (1330, 315)
bot_left  = (1126, 538)
bot_right = (1407, 530)
zone = [top_left, top_right, bot_right, bot_left]

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model.track(frame, persist=True, verbose=False, tracker='bytetrack.yaml')
        boxes = results[0].boxes.xyxy.cpu()
        red_color = (0, 0, 255)
        # y = 308
        # offset = 7

        # counter line
        cv2.polylines(frame, np.array([zone]), True, (255, 0, 0), 2)

        if results[0].boxes.id is not None:
            # Extract prediction results
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()
            annotated_frame = results[0].plot()
            frame = annotated_frame
            
            # Annotator Init
            annotator = Annotator(frame, line_width=2)

            for box, cls, track_id in zip(boxes, clss, track_ids):
                label_name = names[int(cls)]
                if label_name != "person":
                    continue
                # annotator.box_label(box, color=colors(int(cls), True), label=label_name)

                # Store tracking history
                track = track_history[track_id]
                track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                if len(track) > 30:
                    track.pop(0)

                # Plot tracks
                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                # cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
                # cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)
                center_x = int((box[0] + box[2])/2)
                footer_y = int(box[3])

                # if y < (cy + offset) and y > (cy - offset):
                #     if track_id not in counter_down:
                #         cv2.circle(frame, (cx,cy), 4, (0,0,255), -1)
                #         cv2.putText(frame, str(len(counter_down)), (cx,cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,255,255), 2)
                #         counter_down.add(track_id)

        # cv2.putText(frame,('count: ')+ str(len(counter_down)),(60,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, red_color, 1, cv2.LINE_AA) 

        # new_frame_time = time.time()
        # fps = int(1/(new_frame_time-prev_frame_time))
        # prev_frame_time = new_frame_time

        # infor = f"fps: {str(fps)} / count: {str(len(counter_down))}"
        # cv2.putText(frame, infor, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red_color , 1, cv2.LINE_AA) 
        # cv2.imshow('Frame', frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# result.release()
cap.release()
out.release()
cv2.destroyAllWindows()