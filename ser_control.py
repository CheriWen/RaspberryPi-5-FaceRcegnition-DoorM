from adafruit_servokit import ServoKit

# Initialize the servo kit
try:
    kit = ServoKit(channels=16)
except Exception as e:
    print(f"Failed to initialize ServoKit: {e}")
    raise

# The center of the camera frame
camera_center_x = 320
camera_center_y = 240

# Initialize the servo angles
pan_angle = 90
tilt_angle = 90
pan_servo = kit.servo[0]  # Horizontal servo
tilt_servo = kit.servo[1]  # Vertical servo
#pan_servo.angle = pan_angle
#tilt_servo.angle = tilt_angle

def tra_face(x, y, frame_width, frame_height):
    global pan_angle, tilt_angle, camera_center_x, camera_center_y
    face_center_x = x
    face_center_y = y

    # ADjust the pan and tilt angles based on the face position
    pan_offset = face_center_x - camera_center_x
    tilt_offset = face_center_y - camera_center_y

    # Factors to adjust the pan and tilt angles
    pan_angle = 90 + pan_offset * 0.07  # Horizontal adjustment factor
    tilt_angle = 90 + tilt_offset * 0.07  # Vertical adjustment factor

    # Make sure the angles are within the valid range
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
    # Save power by disabling the servos when not in use
    # Like:
    # pan_servo.angle = None
    # tilt_servo.angle = None
