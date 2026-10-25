"""UserService 的实现，模拟从数据库取用户。

对应 MyRPCFromZero 的 myRPCVersion0/server/UserServiceImpl.java。
"""
import random
import uuid

from common.user import User
from service.user_service import UserService


class UserServiceImpl(UserService):
    def get_user_by_user_id(self, user_id: int) -> User:
        print(f"客户端查询了{user_id}的用户")
        # 模拟从数据库中取用户的行为
        return User(
            id=user_id,
            user_name=str(uuid.uuid4()),
            sex=random.choice([True, False]),
        )
