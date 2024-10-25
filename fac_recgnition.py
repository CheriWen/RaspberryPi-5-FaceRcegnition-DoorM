import os
import cv2
import face_recognition
from aud_speeking import speak

# 帧数记录和限制
frame_count = 0
precess_per_n_frames = 10

# 存储所有已知人脸编码和对应的姓名
known_face_encodings = []
known_face_names = []

def load_known_faces(known_faces_dir="/home/Pi/Codes/Fce Recn/Known_Faces"):
    """
    加载known_faces目录下的所有人脸图片并编码
    每个人的名字对应一个文件夹，里面存储该人的人脸图片。
    """
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


def recognize_faces(frame):
    """
    每10帧识别一次
    """
    global frame_count
    frame_count += 1

    if frame_count % precess_per_n_frames == 0:
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
        name = "Unknown"
        first_match_index = next((i for i, is_match in enumerate(matches) if is_match), None)

        if first_match_index is not None:
            name = known_face_names[first_match_index]
        """
        # 如果有匹配，选择匹配到的第一个人脸
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        """

        names.append(name)

    return names, face_locations


def add_new_face(new_name, frame, known_faces_dir="Known_Faces"):
    """
    通过摄像头图像捕捉并保存新的人脸
    name: 新增人脸的名字
    frame: 当前摄像头画面
    known_faces_dir: 已知人脸存储路径
    """
    person_dir = os.path.join(known_faces_dir, new_name)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)

    # 保存新的人脸图片
    image_path = os.path.join(person_dir, f"{new_name}_{len(os.listdir(person_dir)) + 1}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"New face image saved at: {image_path}")

    # 加载保存的人脸并编码
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if face_encodings:
        # 添加新的人脸编码和名字到已知人脸列表
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(new_name)
        print(f"New face added for {new_name}.")
        speak(f"New face added for {new_name}.")
        return True
    else:
        print(f"Failed to encode face for {new_name}.")
        speak(f"Failed to encode face for {new_name}.")
        return False
