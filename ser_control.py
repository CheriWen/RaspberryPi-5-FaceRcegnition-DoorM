from adafruit_servokit import ServoKit

# 初始化舵机
kit = ServoKit(channels=16)
pan_servo = kit.servo[0]  # 水平舵机
tilt_servo = kit.servo[1]  # 垂直舵机

#相机中心点
camera_center_x = 320
camera_center_y = 240

# 初始位置
pan_angle = 90
tilt_angle = 90
pan_servo.angle = pan_angle
tilt_servo.angle = tilt_angle

def tra_face(x, y, frame_width, frame_height):
    global pan_angle, tilt_angle, camera_center_x, camera_center_y
    face_center_x = x
    face_center_y = y

    pan_offset = face_center_x - camera_center_x
    tilt_offset = face_center_y - camera_center_y

    pan_angle = 90 + pan_offset * 0.1
    tilt_angle = 90 + tilt_offset * 0.1

    pan_angle = max(0, min(180, pan_angle))
    tilt_angle = max(0, min(180, tilt_angle))

    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle

def res_position():
    global pan_angle, tilt_angle
    pan_angle = 90
    tilt_angle = 90
    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle

