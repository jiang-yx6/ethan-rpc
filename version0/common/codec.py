"""简单的 JSON 消息编解码。

Java 版本里使用 ObjectOutputStream/ObjectInputStream 做 Java 原生序列化；
Python 里等价且更通用、更安全的做法是用 JSON 序列化。

这里采用「4 字节大端长度前缀 + JSON 字节」的简单帧格式，
避免 TCP 流式传输时半包/粘包导致的解析错误。
"""
import json
import socket
import struct
from typing import Any


def send_obj(sock: socket.socket, obj: Any) -> None:
    """把对象序列化为 JSON 并发送（4 字节长度前缀 + JSON 字节）。"""
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack("!I", len(data)) + data)


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    """精确读取 n 个字节，连接提前关闭时抛出异常。"""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("连接被关闭")
        buf += chunk
    return buf


def recv_obj(sock: socket.socket) -> Any:
    """读取一帧消息并反序列化为 Python 对象。"""
    (length,) = struct.unpack("!I", _recv_exact(sock, 4))
    return json.loads(_recv_exact(sock, length))
