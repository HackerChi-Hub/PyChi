# server/main.py
import asyncio
from handler import handle_client, handle_command_loop

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

# 全局客户端字典，用于管理在线客户端
clients = {}

async def start_server():
    """启动服务端"""
    # 启动异步服务端
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, clients),  # 每个客户端连接交给 handle_client 处理
        '0.0.0.0',
        9000
    )

    # 显示监听信息
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"{Colors.OKCYAN}[INFO] 服务端正在监听：{addrs}{Colors.ENDC}")

    # 显示版权信息
    print(f"""
    {Colors.BOLD}{Colors.HEADER}╔════════════════════════════════════════╗
      欢迎使用  Hackerchi  远程管理工具
      公众号:黑客驰  官网 hackerchi.top
    ╚════════════════════════════════════════╝{Colors.ENDC}
    """)

    # 启动命令交互循环
    asyncio.create_task(handle_command_loop(clients))

    # 持续运行服务端
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print(f"{Colors.WARNING}[INFO] 服务端已关闭{Colors.ENDC}")