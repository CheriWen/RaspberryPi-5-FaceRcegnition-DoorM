import os
import cv2
import face_recognition
from aud_speeking import speak

# Frames per second
frame_count = 0
precess_per_n_frames = 3  # Process every n frames

# Storage the last known face location
known_face_encodings = []
known_face_names = []

# Define the path to the directory containing the known faces
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
                        known_face_encodings.append(face_encodings[0])  # Pick the first face encoding in the image
                        known_face_names.append(person_name)
        print(f"Loaded {len(known_face_names)} faces from {known_faces_dir}")
    except Exception as e:
        print(f"Error loading known faces: {e}")

def recognize_faces(frame):
    """
    Recognize faces in the given frame.
    """
    global frame_count
    frame_count += 1

    # Frame processing
    if frame_count % precess_per_n_frames != 0:
        return [], []

    """
    Detect faces in the frame and encode them.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Transform the frame to RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    encoding_result = face_recognition.face_encodings(rgb_frame, face_locations)

    names = []
    for face_encoding in encoding_result:
        # Check if the face is a match to any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)  # Calculate the confidence level
        name = "Unknown"

        # Pick the best match
        if any(matches):
            best_match_index = distances.argmin() if distances[distances < 0.6].size > 0 else None  # Set the threshold
            if best_match_index is not None and matches[best_match_index]:
                name = known_face_names[best_match_index]

        names.append(name)

    return names, face_locations

def add_new_face(new_name, frame, known_faces_dir=KNOWN_FACES_DIR):
    """
    Capture and save a new face image.
    name: name of the person
    frame: the frame containing the face
    known_faces_dir: path to the directory containing known faces
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

    # Save the new face image
    image_path = os.path.join(person_dir, f"{new_name}_{len(os.listdir(person_dir)) + 1}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"New face image saved at: {image_path}")

    # Load and encode the new face
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            # Add the new face encoding to the list
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
