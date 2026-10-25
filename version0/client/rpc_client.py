"""RPC 客户端。

对应 MyRPCFromZero 的 myRPCVersion0/client/RPCClient.java：
1. 建立 Socket 连接
2. 传一个随机 id 给服务端
3. 服务端查询数据，返回对应的 User 对象
"""
import random
import socket

from common.codec import recv_obj, send_obj

HOST = "127.0.0.1"
PORT = 8899


def main() -> None:
    try:
        # 建立 Socket 连接
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            # 传给服务器一个随机 id
            send_obj(sock, random.randint(0, 2**31 - 1))
            # 服务器查询数据，返回对应的对象
            user = recv_obj(sock)
            print(f"服务端返回的User:{user}")
    except (OSError, ValueError, ConnectionError) as e:
        print(f"客户端启动失败: {e}")


if __name__ == "__main__":
    main()
