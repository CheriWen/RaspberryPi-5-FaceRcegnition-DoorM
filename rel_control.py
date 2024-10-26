import RPi.GPIO as GPIO
import time
import threading

# Definitions
RELAY_PIN = 17
DOOR_OPEN_TIME = 5  # The time the door stays open in seconds

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)  # Close the door initially

def open_door():
    """
    Opens the door
    """
    try:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Open the door
        print("Door opened")
        
        # Lauch a separate thread to close the door after a delay
        threading.Thread(target=close_door_after_delay).start()
        
        return True  # Door opened successfully
    except Exception as e:
        print(f"Error while opening the door: {e}")
        return False  # Door opening failed

def close_door_after_delay():
    """
    Delays the door closing
    """
    time.sleep(DOOR_OPEN_TIME)
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Close the door
    print("Door closed")

def cleanup(clean=False):
    """
    Cleans up the GPIO state
    clean: States whether to clean up the GPIO state or not
    """
    if clean:
        GPIO.cleanup()
        print("GPIO cleaned up")

# Test
if __name__ == "__main__":
    try:
        open_door()
        # Other code
        time.sleep(10)  # Shit
    finally:
        cleanup(clean=True)  # Clean up the GPIO state
