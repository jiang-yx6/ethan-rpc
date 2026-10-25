# ethan-rpc

用 Python 实现的一个「最简单的 RPC 调用」，与 Java 项目
[MyRPCFromZero](../MyRPCFromZero) 的 `myRPCVersion0` 一一对应。

一个 RPC 最最简单的过程是：客户端**调用**服务端的一个方法，服务端把执行结果返回给客户端。
这里用一个「从数据库取用户」的例子，模拟一次完整的 RPC 流程。

## 目录结构（与 Java 版对应）

| Java（myRPCVersion0）        | Python（ethan-rpc）                    | 说明                       |
| ---------------------------- | -------------------------------------- | -------------------------- |
| `common/User.java`           | `common/user.py`                       | 客户端与服务端共有的实体   |
| `service/UserService.java`   | `service/user_service.py`              | 服务接口                   |
| `server/UserServiceImpl.java`| `server/user_service_impl.py`          | 服务接口的实现             |
| `server/RPCServer.java`      | `server/rpc_server.py`                 | BIO 方式的 RPC 服务端      |
| `client/RPCClient.java`      | `client/rpc_client.py`                 | RPC 客户端                 |
| （ObjectOutputStream 序列化） | `common/codec.py`                      | 消息编解码（JSON）         |

## 流程

1. 客户端建立 Socket 连接，把一个随机 `id` 传给服务端；
2. 服务端收到 `id`，调用 `UserServiceImpl.get_user_by_user_id`，模拟从数据库取出一条
   `User`（随机 `userName`、随机 `sex`），写回客户端；
3. 客户端打印服务端返回的 `User`。

## 运行

先启动服务端（在 `ethan-rpc` 目录下）：

```bash
python -m server.rpc_server
```

再启动客户端（另一个终端，同样在 `ethan-rpc` 目录下）：

```bash
python -m client.rpc_client
```

客户端输出示例：

```
服务端返回的User:{'id': 123456789, 'userName': '0e3f...', 'sex': True}
```

服务端输出示例：

```
服务端启动了
客户端查询了123456789的用户
```

## 与 Java 版的差异

- Java 用 `ObjectOutputStream`/`ObjectInputStream` 做原生序列化，直接传输 `int` 与
  `User` 对象；Python 用 JSON 序列化，通过 `common/codec.py` 统一以
  「4 字节长度前缀 + JSON 字节」成帧，避免 TCP 半包/粘包问题。
- Java 用 `new Thread(...)` 每连接开一个线程，Python 用 `threading.Thread`，逻辑一致。

> 这个版本及其不完善（消息格式没统一、只能调用唯一确定的方法、返回值只支持 User），
> 后续版本会像 Java 项目那样逐步抽象出 Request/Response 与动态代理。

## 常见问题

- **Windows 下中文乱码**：cmd/PowerShell 默认使用 GBK 代码页。若控制台中文乱码，先执行
  `chcp 65001` 切换到 UTF-8，或使用 `python -X utf8 -m server.rpc_server` / `client.rpc_client` 运行。
