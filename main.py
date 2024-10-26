import cv2
from picamera2 import Picamera2
from fac_recgnition import recognize_faces, load_known_faces, add_new_face
from cam_tracking import det_face, get_frame, sho_frame
#from aud_speeking import speak
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
from rel_control import open_door, close_door_after_delay
from ser_control import tra_face

# Create a thread-safe queue to store the results of face recognition
result_queue = queue.Queue()

class CameraError(Exception):
    pass

class IOError(Exception):
    pass

def face_processing_thread(frame):
    """Put the face recognition result into the queue"""
    try:
        names, face_locations = recognize_faces(frame)
        result_queue.put((names, face_locations))  # Put the result into the queue
    except Exception as e:
        print(f"Error during face processing: {e}")

def main():
    load_known_faces()  # Load known faces from the database

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                # Get a frame from the camera
                frame = get_frame()

                # Submit the frame to the face recognition thread
                executor.submit(face_processing_thread, frame)

                # Process the results from the queue (non-blocking)
                while not result_queue.empty():
                    names, face_locations = result_queue.get()
                    handle_recognition_results(names, face_locations, frame)

                    # Trace the face
                    if face_locations:   
                        #Test if the face is in the database
                        print(face_locations)
                        
                        det_face(face_locations)
                        
                # Show the frame with the face locations
                sho_frame(frame, face_locations)

                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except CameraError as ce:
        print(f"Camera error: {ce}")
    except IOError as ioe:
        print(f"IO error: {ioe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cv2.destroyAllWindows

def handle_recognition_results(names, face_locations, frame):
    """Process the results of face recognition"""
    for name in names:
        if name != "Unknown":
            print(f"Hello, {name}!")
            # Open the door
            open_door()
            # 将说话操作放入队列，批量处理
            #threading.Thread(target=speak, args=(f"Hello, {name}!",)).start()
        else:
            print("I don't know you.")
            print("Leave or press the CorrectKey to add a new face.")

            # 将输入操作放入队列，批量处理
            if cv2.waitKey(1) & 0xFF == ord('a'):
                new_name = input("Enter the name of the new person: ")
                if add_new_face(new_name, frame):
                    print(f"New person {new_name} added!")
                    #threading.Thread(target=speak, args=(f"New person {new_name} added!",)).start()
                else:
                    print(f"Failed to add new face.")
                    #threading.Thread(target=speak, args=(f"Failed to add new face.",)).start()

if __name__ == '__main__':
    main()
