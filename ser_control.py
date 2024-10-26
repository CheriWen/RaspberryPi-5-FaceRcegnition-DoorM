from adafruit_servokit import ServoKit

# 初始化舵机
try:
    kit = ServoKit(channels=16)
except Exception as e:
    print(f"Failed to initialize ServoKit: {e}")
    raise

# 相机中心点
camera_center_x = 320
camera_center_y = 240

# 初始位置
pan_angle = 90
tilt_angle = 90
pan_servo = kit.servo[0]  # 水平舵机
tilt_servo = kit.servo[1]  # 垂直舵机
#pan_servo.angle = pan_angle
#tilt_servo.angle = tilt_angle

def tra_face(x, y, frame_width, frame_height):
    global pan_angle, tilt_angle, camera_center_x, camera_center_y
    face_center_x = x
    face_center_y = y

    # 偏移量调整，允许用户根据实际跟踪效果进行修改
    pan_offset = face_center_x - camera_center_x
    tilt_offset = face_center_y - camera_center_y

    # 可以根据实际效果调节缩放因子
    pan_angle = 90 + pan_offset * 0.08  # 调整因子
    tilt_angle = 90 + tilt_offset * 0.08  # 调整因子

    # 确保角度在舵机支持的范围内
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
    # 可以考虑在空闲时关闭电机输出信号以节省电力
    # 如果支持，可添加此功能，例如：
    # pan_servo.angle = None
    # tilt_servo.angle = None
