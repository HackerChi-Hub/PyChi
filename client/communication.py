#client\communication.py
# client/communication.py

def send_data_with_header(sock, data):
    """发送带有长度头的消息"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    header = f"{len(data):<10}".encode('utf-8')
    sock.sendall(header + data)

def receive_data_with_header(sock):
    """接收带有长度头的消息"""
    header = sock.recv(10)
    if not header:
        return None
    total_size = int(header.strip())
    received_data = b""
    while len(received_data) < total_size:
        chunk = sock.recv(1024)
        if not chunk:
            break
        received_data += chunk
    return received_data