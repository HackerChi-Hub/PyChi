# PyChi
基于 Python 的Hackerchi远程管理工具：PyChi 远程管理系统
![image](https://github.com/user-attachments/assets/b31c0104-f8f2-446c-8eaa-38fe53d4c7e0)
![image](https://github.com/user-attachments/assets/2346dc5d-cff4-4a51-83dc-991f24c90d3b)

## 引言

在现代 IT 环境中，远程管理工具是开发者和运维人员必不可少的利器。本文将为大家介绍一个基于 Python 构建的多功能远程管理工具 PyChi，它能够让你轻松地对远程客户端进行管理操作，包括文件管理、系统命令执行、截图、录音等功能。


## 软件简介

PyChi 是一个基于异步通信的远程管理工具，采用了 Python 的 `asyncio` 库实现高效的客户端-服务端通信。通过它，你可以：

- 实时管理和控制多台客户端设备
- 执行远程命令
- 传输文件
- 获取系统信息
- 进行多种实用操作，如截图和录音

### 项目结构

项目代码分为两部分：**服务端** 和 **客户端**。

- **服务端**：监听客户端连接并处理管理请求。
- **客户端**：连接服务端并执行收到的命令。

主要文件介绍如下：

- `server/main.py`：服务端主程序，启动监听并处理客户端连接。
- `server/handler.py`：服务端核心逻辑，包括命令处理和客户端管理。
- `server/communication.py`：服务端与客户端通信的底层实现。
- `client/main.py`：客户端主程序，连接服务端并执行指令。
- `client/commands.py`：客户端支持的功能实现，如文件操作、截图等。
- `client/communication.py`：客户端与服务端通信的底层实现。

---

## 服务端功能

服务端是 PyChi的核心组件，负责管理所有客户端连接并发送控制指令。

### 1. **多客户端管理**

服务端支持同时管理多个客户端，并提供以下功能：

- 显示所有在线客户端
- 选择目标客户端进行操作
- 自定义命令交互

### 2. **命令交互**

通过服务端，你可以向客户端发送多种命令。可以输入 `help` 查看详细命令列表：

### 系统信息与工具

- `info`：获取客户端的操作系统和主机信息。
- `screenshot`：截屏并保存为图片（支持 Windows 和 macOS）。
- `record <duration>`：录音并保存为音频文件，`<duration>` 为录音时长（默认 5 秒）。
- `scan_network`：扫描客户端所在局域网的在线设备。

### 文件操作

- `list <directory>`：列出客户端指定目录的内容。
- `create <file_path>`：创建一个新文件。
- `delete <file_path>`：删除文件或文件夹。
- `read <file_path>`：读取文件内容，支持多种编码。
- `upload <file_path>`：从服务端上传文件到客户端。
- `download <file_path>`：从客户端下载文件到服务端。

### 系统命令

- `cmd <system_command>`：执行客户端操作系统的命令，例如 `ls` 或 `dir`。

---

## 客户端功能

客户端是 PyChi 的执行端，负责连接服务端并响应指令。以下是客户端支持的主要功能：

### 1. **文件管理**

客户端支持多种文件操作，包括：

- 列出目录内容
- 创建、删除文件或文件夹
- 读取文件内容（支持多种编码）
- 文件上传与下载

### 2. **系统工具**

### 局域网扫描

通过 `scan_network` 命令，客户端可以扫描其所在的局域网，返回在线设备的 IP 地址列表。

### 截屏

通过 `screenshot` 命令，客户端可以截取当前屏幕并保存为图片文件。支持的系统包括 **Windows** 和 **macOS**。

### 录音

通过 `record` 命令，客户端可以录制音频文件，并保存为 `.wav` 格式。

### 3. **命令执行**

客户端可以执行服务端发送的系统命令。例如：

- 在 Windows 上执行 `dir` 查看目录内容
- 在 Linux/Mac 上执行 `ls` 列出文件

---

## 异步通信实现

PyChi的通信机制基于异步编程，确保在多客户端连接时仍然高效稳定。下面是其核心实现：

### 1. **消息传输协议**

通信采用固定长度的消息头，消息头包含数据长度，方便分块接收完整数据：

- 数据发送：`send_data_with_header`
- 数据接收：`receive_data_with_header`

```python
# 示例：发送数据
header = f"{len(data):<10}".encode('utf-8')
writer.write(header + data)
```

### 2. **服务端管理客户端**

服务端维护一个全局字典 `clients`，存储所有在线客户端的连接信息：

```python
clients[addr] = (reader, writer)  # 客户端地址作为键
```

服务端可通过选择客户端并发送指令来实现交互。

---

## 使用方法

### 1. 部署服务端

在服务器上运行服务端程序：

```bash
python server/main.py
```

### 2. 部署客户端

在客户端设备上运行客户端程序：

```bash
python client/main.py
```

### 3. 连接管理

客户端运行后会尝试连接服务端，连接成功后，服务端可对客户端进行管理操作。

---

## 适用场景

1. **远程技术支持**：管理员可以通过该工具帮助用户解决系统问题。
2. **远程文件管理**：无需物理接触设备即可操作文件。
3. **系统监控**：通过局域网扫描、截屏等功能了解设备状态。
4. **教育与演示**：在编程教学中展示异步编程和客户端-服务端通信的实现。

---

## 注意事项

1. **安全性**：目前工具未实现加密通信，适用于受信任的局域网环境。建议后续引入 TLS 加密。
2. **跨平台支持**：部分功能（如截图）在不同操作系统上的兼容性有所差异。
3. **依赖库**：请确保安装必要的依赖库，详见 `requirements.txt` 文件。
