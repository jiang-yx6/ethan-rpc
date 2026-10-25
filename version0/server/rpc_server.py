"""BIO 方式的 RPC 服务端。

对应 MyRPCFromZero 的 myRPCVersion0/server/RPCServer.java：
1. 监听 8899 端口
2. accept 到连接后，为每个连接开启一个线程去处理
3. 读取客户端传来的 id，调用 UserService 获取 User，写回客户端
"""
import socket
import threading

from common.codec import recv_obj, send_obj
from server.user_service_impl import UserServiceImpl

HOST = "127.0.0.1"
PORT = 8899


def handle_client(conn: socket.socket, user_service: UserServiceImpl) -> None:
    try:
        # 读取客户端传过来的 id
        user_id = recv_obj(conn)
        user = user_service.get_user_by_user_id(user_id)
        # 写入 User 对象给客户端
        send_obj(conn, user.to_dict())
    except (OSError, ValueError, ConnectionError) as e:
        print(f"从IO中读取数据错误: {e}")
    finally:
        conn.close()


def main() -> None:
    user_service = UserServiceImpl()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # 允许端口复用，方便快速重启
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print("服务端启动了")
        # BIO 的方式监听 Socket
        while True:
            conn, _addr = server.accept()
            # 开启一个线程去处理
            threading.Thread(
                target=handle_client, args=(conn, user_service), daemon=True
            ).start()


if __name__ == "__main__":
    main()
