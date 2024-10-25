from adafruit_servokit import ServoKit

# 初始化舵机
kit = ServoKit(channels=16)
pan_servo = 0  # 水平舵机
tilt_servo = 1  # 垂直舵机

# 初始位置
pan_angle = 90
tilt_angle = 90
kit.servo[pan_servo].angle = pan_angle
kit.servo[tilt_servo].angle = tilt_angle

def tra_face(x, y, frame_width, frame_height):
    global pan_angle, tilt_angle
    x_offset = x - frame_width // 2
    y_offset = y - frame_height // 2

    if x_offset > 50:
        pan_angle -= 2
    elif x_offset < -50:
        pan_angle += 2

    if y_offset > 50:
        tilt_angle += 2
    elif y_offset < -50:
        tilt_angle -= 2

    pan_angle = max(0, min(180, pan_angle))
    tilt_angle = max(0, min(180, tilt_angle))

    kit.servo[pan_servo].angle = pan_angle
    kit.servo[tilt_servo].angle = tilt_angle

def res_position():
    global pan_angle, tilt_angle
    pan_angle = 90
    tilt_angle = 90
    kit.servo[pan_servo].angle = pan_angle
    kit.servo[tilt_servo].angle = tilt_angle
