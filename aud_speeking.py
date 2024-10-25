import os

def speak(text, language='en-us', speed=150):
    """
    使用 espeak 进行文本转语音。
    
    参数:
        text (str): 要朗读的文本。
        language (str): 语音语言，默认是 'en-us'。
        speed (int): 语音速度，默认是 150。
    """
    try:
        # 构造 espeak 命令
        command = f"espeak -v {language} -s {speed} '{text}'"
        os.system(command)
    except Exception as e:
        print(f"Error occurred while speaking: {e}")
