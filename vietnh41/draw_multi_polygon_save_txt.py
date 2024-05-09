import cv2
import numpy as np


# Khởi tạo danh sách các điểm
points = []
polygons = []  # Danh sách chứa các polygons

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Thêm điểm vào danh sách
        points.append((x, y))
        
        # Vẽ điểm trên ảnh
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('image', img)

    if event == cv2.EVENT_RBUTTONDOWN:
        # Vẽ đa giác khi nhấn phím enter
        if len(points) > 1:
            cv2.polylines(img, [np.array(points)], True, (255, 0, 0), 2)
            cv2.imshow('image', img)
            polygons.append(points.copy())  # Lưu polygon hiện tại
            points.clear()  # Xóa các điểm sau khi vẽ

# Tạo cửa sổ hiển thị ảnh
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_event)

# Tải ảnh
img = cv2.imread('imgsave.jpg')
cv2.imshow('image', img)

# Chờ phím enter được nhấn
while True:
    key = cv2.waitKey(1)
    if key == 13:  # Phím enter
        if len(points) > 1:
            cv2.polylines(img, [np.array(points)], True, (255, 0, 0), 2)
            cv2.imshow('image', img)
            polygons.append(points.copy())  # Lưu polygon hiện tại
            points.clear()  # Xóa các điểm sau khi vẽ
    elif key == 27:  # Phím ESC để thoát
        break

cv2.destroyAllWindows()

# Lưu tọa độ vào file
with open('vietnh41/polygons.txt', 'w') as file:
    for polygon in polygons:
        for point in polygon:
            file.write(f"{point[0]}, {point[1]}\n")
        file.write("---\n")