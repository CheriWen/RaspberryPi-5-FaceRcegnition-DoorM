import cv2
from picamera2 import Picamera2
from ser_control import tra_face, res_position

picam2 = Picamera2()
picam2.start()

frame_width = 640
frame_height = 480

def det_face(face_locations):
    if face_locations:
        '''
        # Choose the face closest to the center of the frame
        center_x = frame_width // 2
        center_y = frame_height // 2

        closest_face = min(face_locations, key=lambda box: (
            abs((box[0] + box[2]) // 2 - center_x) + abs((box[1] + box[3]) // 2 - center_y)
        ))

        (top, right, bottom, left) = closest_face
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        tra_face(center_x, center_y, frame_width, frame_height)
        '''
        print(face_locations)
        (top, right, bottom, left) = max(face_locations, key=lambda box: (box[1] - box[3]) * (box[2] - box[0]))
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        tra_face(center_x, center_y, frame_width, frame_height)

    else:
        res_position()

def get_frame():
    try:
        return cv2.flip(picam2.capture_array(), 0)
    except Exception as e:
        print(f"Error capturing frame: {e}")
        return None

def sho_frame(frame, face_locations):
    if face_locations:
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 3)
    
    # Transform the frame from BGR to RGB
    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('Frame', RGB_frame)

def cleanup():
    picam2.stop()  # Stop the camera
    cv2.destroyAllWindows()  # Clean up any open windows
