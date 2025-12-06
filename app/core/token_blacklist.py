"""
Token黑名单管理模块
用于存储已登出的token，防止其继续被使用
"""
from typing import Set

# 存储被加入黑名单的token
_token_blacklist: Set[str] = set()

def add_token_to_blacklist(token: str) -> None:
    """将token加入黑名单"""
    _token_blacklist.add(token)

def is_token_blacklisted(token: str) -> bool:
    """检查token是否在黑名单中"""
    return token in _token_blacklist

def remove_token_from_blacklist(token: str) -> None:
    """从黑名单移除token"""
    _token_blacklist.discard(token)

def clear_blacklist() -> None:
    """清空黑名单"""
    _token_blacklist.clear()
