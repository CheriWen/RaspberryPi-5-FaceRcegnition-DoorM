import cv2
from picamera2 import Picamera2
from fac_recgnition import recognize_faces, load_known_faces, add_new_face
from cam_tracking import det_face, get_frame, sho_frame
#from rel_control import open_door, cleanup
from aud_speeking import speak
import threading
from concurrent.futures import ThreadPoolExecutor

"""
def process_faces(frame):
    names, face_locations = recognize_faces(frame)

    for name in names:
        if name != "Unknown":
            speak(f"Hello, {name}!")
            #open_door()
        else:
            speak("I don't know you.")
            speak("Leave or press the passkey to add a new face.")
            # 按 'a' 键录入新面孔
            if cv2.waitKey(1) & 0xFF == ord('a'):
                new_name = input("Enter the name of the new person: ")
                if add_new_face(new_name, frame):
                    speak(f"New person {new_name} added!")
                else:
                    speak("Failed to add new face.")
"""

def main():
    
    # Load known faces
    load_known_faces()

    face_locations = []

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                # Get the frame from the camera
                frame = get_frame()

                # 启动新线程处理人脸识别，并更新 face_locations
                def face_processing_thread(frame):
                    nonlocal face_locations
                    names, face_locations = recognize_faces(frame)
                    # Known faces
                    for name in names:
                        if name != "Unknown":
                            print(f"Hello, {name}!")
                            speak(f"Hello, {name}!")
                            #open_door()
                        else:
                            print("I don't know you.")
                            print("Leave or press the CorrectKey to add a new face.")
                            # Add a new face
                            if cv2.waitKey(1) & 0xFF == ord('a'):
                                new_name = input("Enter the name of the new person: ")
                                if add_new_face(new_name, frame):
                                    print(f"New person {new_name} added!")
                                    speak(f"New person {new_name} added!")
                                else:
                                    print(f"Failed to add new face.")
                                    speak(f"Failed to add new face.")

                # 启动新线程处理人脸识别并扔到线程池里面
                future = executor.submit(face_processing_thread, frame)

                # Wait for the thread to complete
                face_locations = future.result()

                # 人脸跟踪
                det_face(face_locations)

                # Show the frame with the face locations
                sho_frame(frame, face_locations)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

    finally:
        # release the camera resources
        #cleanup()
        cv2.destroyAllWindows()
        del frame

if __name__ == '__main__':
    main()
