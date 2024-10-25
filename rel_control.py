import RPi.GPIO as GPIO
import time
import threading

# 定义常量管理引脚号
RELAY_PIN = 17
DOOR_OPEN_TIME = 5  # 继电器开启时间，单位为秒

# GPIO 设置
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # 默认关闭继电器

def open_door():
    """
    控制门打开
    """
    try:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # 打开门
        print("Door opened")
        
        # 启动一个线程来关闭门，避免阻塞主线程
        threading.Thread(target=close_door_after_delay).start()
        
        return True  # 返回状态表示门已打开
    except Exception as e:
        print(f"Error while opening the door: {e}")
        return False  # 返回状态表示打开门失败

def close_door_after_delay():
    """
    延时关闭门
    """
    time.sleep(DOOR_OPEN_TIME)
    GPIO.output(RELAY_PIN, GPIO.LOW)  # 关闭门
    print("Door closed")

def cleanup(clean=False):
    """
    清理 GPIO 设置
    clean: 是否清理 GPIO 状态
    """
    if clean:
        GPIO.cleanup()
        print("GPIO cleaned up")

# 测试示例
if __name__ == "__main__":
    try:
        open_door()
        # 其他业务逻辑
        time.sleep(10)  # 让程序运行一段时间以观察门的状态
    finally:
        cleanup(clean=True)  # 清理 GPIO 状态
