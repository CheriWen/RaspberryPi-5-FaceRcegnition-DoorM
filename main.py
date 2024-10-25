import cv2
from picamera2 import Picamera2
from fac_recgnition import recognize_faces, load_known_faces, add_new_face
from cam_tracking import det_face, get_frame, sho_frame
from aud_speeking import speak
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

# 创建一个线程安全的队列，用于存储人脸识别结果
result_queue = queue.Queue()

class CameraError(Exception):
    pass

class IOError(Exception):
    pass

def face_processing_thread(frame):
    """处理人脸识别并将结果放入队列"""
    try:
        names, face_locations = recognize_faces(frame)
        result_queue.put((names, face_locations))  # 将结果放入队列
    except Exception as e:
        print(f"Error during face processing: {e}")

def main():
    load_known_faces()  # 加载已知人脸

    picam2 = Picamera2()  # 创建摄像头实例
    picam2.start()        # 启动摄像头

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                # 获取摄像头帧
                frame = get_frame()

                # 提交人脸识别任务到线程池
                executor.submit(face_processing_thread, frame)

                # 处理队列中的识别结果（非阻塞）
                while not result_queue.empty():
                    names, face_locations = result_queue.get()
                    handle_recognition_results(names, face_locations, frame)

                # 人脸跟踪
                if face_locations:  # 确保只在有识别结果时调用
                    det_face(face_locations)

                # 显示带有人脸位置的帧
                sho_frame(frame, face_locations)

                # 按 'q' 键退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except CameraError as ce:
        print(f"Camera error: {ce}")
    except IOError as ioe:
        print(f"IO error: {ioe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        picam2.close()       # 关闭摄像头
        cv2.destroyAllWindows()  # 清理OpenCV窗口

def handle_recognition_results(names, face_locations, frame):
    """处理识别结果"""
    for name in names:
        if name != "Unknown":
            print(f"Hello, {name}!")
            # 将说话操作放入队列，批量处理
            threading.Thread(target=speak, args=(f"Hello, {name}!",)).start()
        else:
            print("I don't know you.")
            print("Leave or press the CorrectKey to add a new face.")

            # 将输入操作放入队列，批量处理
            if cv2.waitKey(1) & 0xFF == ord('a'):
                new_name = input("Enter the name of the new person: ")
                if add_new_face(new_name, frame):
                    print(f"New person {new_name} added!")
                    threading.Thread(target=speak, args=(f"New person {new_name} added!",)).start()
                else:
                    print(f"Failed to add new face.")
                    threading.Thread(target=speak, args=(f"Failed to add new face.",)).start()

if __name__ == '__main__':
    main()
