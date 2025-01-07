# server/communication.py

# 定义 ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

async def send_data_with_header(writer, data):
    """发送带有长度头的消息"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    header = f"{len(data):<10}".encode('utf-8')  # 固定 10 字节的头部，表示消息长度
    try:
        writer.write(header + data)
        await writer.drain()
        print(f"{Colors.OKGREEN}[INFO] 数据已成功发送到客户端{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] 发送数据失败：{e}{Colors.ENDC}")

async def receive_data_with_header(reader):
    """接收带有长度头的消息"""
    try:
        header = await reader.readexactly(10)
        if not header:
            return None
        total_size = int(header.strip())
        received_data = await reader.readexactly(total_size)
        print(f"{Colors.OKGREEN}[INFO] 已成功接收客户端数据{Colors.ENDC}")
        return received_data
    except Exception as e:
        print(f"{Colors.FAIL}[ERROR] 接收数据失败：{e}{Colors.ENDC}")
        return None