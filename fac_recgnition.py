import os
import cv2
import face_recognition
from aud_speeking import speak

# 帧数记录和限制
frame_count = 0
precess_per_n_frames = 3  # 每10帧处理一次

# 存储所有已知人脸编码和对应的姓名
known_face_encodings = []
known_face_names = []

# 常量定义
KNOWN_FACES_DIR = "/home/Pi/Codes/Fce Recn/Known_Faces"

def load_known_faces(known_faces_dir=KNOWN_FACES_DIR):
    """
    加载known_faces目录下的所有人脸图片并编码
    每个人的名字对应一个文件夹，里面存储该人的人脸图片。
    """
    try:
        for person_name in os.listdir(known_faces_dir):
            person_dir = os.path.join(known_faces_dir, person_name)

            if os.path.isdir(person_dir):
                for image_file in os.listdir(person_dir):
                    image_path = os.path.join(person_dir, image_file)
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)

                    if face_encodings:
                        known_face_encodings.append(face_encodings[0])  # 只取第一张脸的编码
                        known_face_names.append(person_name)
        print(f"Loaded {len(known_face_names)} faces from {known_faces_dir}")
    except Exception as e:
        print(f"Error loading known faces: {e}")

def recognize_faces(frame):
    """
    每10帧识别一次
    """
    global frame_count
    frame_count += 1

    # 修正帧率限制逻辑
    if frame_count % precess_per_n_frames != 0:
        return [], []

    """
    检测并识别人脸，返回人名和人脸位置
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 将BGR转换为RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    encoding_result = face_recognition.face_encodings(rgb_frame, face_locations)

    names = []
    for face_encoding in encoding_result:
        # 检查每张检测到的人脸是否与已知人脸匹配
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)  # 获取距离
        name = "Unknown"

        # 使用最小距离作为最佳匹配
        if any(matches):
            best_match_index = distances.argmin() if distances[distances < 0.6].size > 0 else None  # 设定距离阈值
            if best_match_index is not None and matches[best_match_index]:
                name = known_face_names[best_match_index]

        names.append(name)

    return names, face_locations

def add_new_face(new_name, frame, known_faces_dir=KNOWN_FACES_DIR):
    """
    通过摄像头图像捕捉并保存新的人脸
    name: 新增人脸的名字
    frame: 当前摄像头画面
    known_faces_dir: 已知人脸存储路径
    """
    # 先检测人脸是否存在
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if not face_encodings:
        print("No face detected for saving.")
        #speak("No face detected for saving.")
        return False

    person_dir = os.path.join(known_faces_dir, new_name)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)

    # 保存新的人脸图片
    image_path = os.path.join(person_dir, f"{new_name}_{len(os.listdir(person_dir)) + 1}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"New face image saved at: {image_path}")

    # 加载保存的人脸并编码
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            # 添加新的人脸编码和名字到已知人脸列表
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(new_name)
            print(f"New face added for {new_name}.")
            #speak(f"New face added for {new_name}.")
            return True
        else:
            print(f"Failed to encode face for {new_name}.")
            #speak(f"Failed to encode face for {new_name}.")
            return False
    except Exception as e:
        print(f"Error adding new face: {e}")
