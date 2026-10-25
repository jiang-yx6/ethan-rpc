"""UserService 服务接口。

对应 MyRPCFromZero 的 myRPCVersion0/service/UserService.java：
客户端通过这个接口调用服务端的实现类。
"""
from abc import ABC, abstractmethod

from common.user import User


class UserService(ABC):
    @abstractmethod
    def get_user_by_user_id(self, user_id: int) -> User:
        """根据 id 查询用户。"""
        raise NotImplementedError
