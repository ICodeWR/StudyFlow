#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2025 ICodeWR（微信公众号同名）

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Module/Script Name: auth.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day08 exexample Script.

# utils/auth.py

import streamlit as st
from enum import IntEnum
import hashlib


def hash_password(password: str) -> str:
    """使用SHA-256进行密码哈希（生产环境建议使用bcrypt）"""
    return hashlib.sha256(password.encode()).hexdigest()

# 角色权限等级枚举
class RoleLevel(IntEnum):
    GUEST = 0
    USER = 1
    ADMIN = 2

# 预定义角色权限映射
ROLE_PERMISSIONS = {
    "guest": RoleLevel.GUEST,
    "user": RoleLevel.USER,
    "admin": RoleLevel.ADMIN
}

# 示例用户数据库（生产环境应使用真实数据库）
DEMO_USERS = {
    "admin": {
        "password": hash_password("admin123"),  # 密码哈希值
        "role": "admin",
        "display_name": "系统管理员"
    },
    "user1": {
        "password": hash_password("user123"),
        "role": "user",
        "display_name": "普通用户"
    }
}


def check_login(username: str, password: str) -> bool:
    """验证用户登录凭证"""
    user = DEMO_USERS.get(username)
    
    # 用户不存在
    if not user:
        st.error("用户不存在")
        return False
    
    # 验证密码哈希
    if user["password"] != hash_password(password):
        st.error("密码错误")
        return False
    
    # 更新会话状态
    st.session_state.auth = {
        "logged_in": True,
        "username": username,
        "role": user["role"],
        "display_name": user["display_name"]
    }
    return True

def check_permission(required_level: RoleLevel) -> bool:
    """检查当前用户权限是否满足要求"""
    if not st.session_state.auth.get("logged_in"):
        return False
    
    current_role = st.session_state.auth["role"]
    current_level = ROLE_PERMISSIONS.get(current_role, RoleLevel.GUEST)
    
    return current_level >= required_level

def logout():
    """执行注销操作"""
    st.session_state.auth = {
        "logged_in": False,
        "role": "guest"
    }
    st.rerun()

# 权限装饰器
def require_login(func):
    """装饰器：需要登录才能访问"""
    def wrapper(*args, **kwargs):
        if not st.session_state.auth.get("logged_in"):
            st.error("请先登录系统")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role: str):
    """装饰器：需要特定角色才能访问"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.auth.get("role") != required_role:
                st.error("权限不足")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator

