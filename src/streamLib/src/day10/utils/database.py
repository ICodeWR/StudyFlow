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

# Module/Script Name: database.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import sqlite3
import pandas as pd
import streamlit as st
from functools import wraps
from utils.security import hash_password


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            st.error(f"数据库错误: {str(e)}")
            raise
        except Exception as e:
            st.error(f"操作失败: {str(e)}")
            raise
    return wrapper

@st.cache_resource(show_spinner=False)
def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect("data.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@handle_db_errors
def query_db(query, params=None, _conn=None):
    """执行查询并返回DataFrame"""
    conn = _conn or get_connection()
    return pd.read_sql(query, conn, params=params)

@handle_db_errors
def execute_db(query, params=None, _conn=None):
    """执行非查询SQL语句"""
    conn = _conn or get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    return cursor.rowcount

def init_database():
    """初始化数据库表结构"""
    conn = get_connection()
    
    # 创建用户表
    execute_db("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'viewer',
        status TEXT NOT NULL DEFAULT 'active',
        region TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """, _conn=conn)
    
    # 创建销售表
    execute_db("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        amount REAL NOT NULL,
        date DATE NOT NULL,
        region TEXT NOT NULL
    )
    """, _conn=conn)
    
    # 添加示例数据
    if not query_db("SELECT COUNT(*) as count FROM users", _conn=conn).iloc[0]['count']:
        execute_db("""
        INSERT INTO users (username, password, role, region) 
        VALUES (?, ?, ?, ?)
        """, ("admin", hash_password("admin123"), "admin", "华东"), _conn=conn)
        
        # 添加示例销售数据
        import random
        from datetime import datetime, timedelta
        
        regions = ["华东", "华北", "华南", "华中", "西部"]
        products = ["P1001", "P1002", "P1003", "P1004", "P1005"]
        
        for i in range(100):
            date = datetime.now() - timedelta(days=random.randint(0, 30))
            execute_db("""
            INSERT INTO sales (product_id, quantity, amount, date, region)
            VALUES (?, ?, ?, ?, ?)
            """, (
                random.choice(products),
                random.randint(1, 10),
                round(random.uniform(100, 1000), 2),
                date.strftime("%Y-%m-%d"),
                random.choice(regions)
            ), _conn=conn)
    
    conn.commit()

# 初始化数据库
init_database()

