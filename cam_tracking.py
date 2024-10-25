import cv2
from picamera2 import Picamera2
from ser_control import tra_face, res_position
picam2 = Picamera2()
picam2.start()

frame_width = 640
frame_height = 480

def det_face(face_locations):
    if face_locations:
        (top, right, bottom, left) = max(face_locations, key=lambda box: (box[1] - box[3]) * (box[2] - box[0]))
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        tra_face(center_x, center_y, frame_width, frame_height)
        
    else:
        res_position()

def get_frame():
    return picam2.capture_array()

def sho_frame(frame,face_locations):
    if face_locations:
        for (x, y, w, h) in face_locations:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('Frame', RGB_frame)
