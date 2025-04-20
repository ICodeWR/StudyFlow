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

# Module/Script Name: init_db.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: Remi day8 exexample Script.

import sqlite3

# 连接数据库（如果不存在则创建）
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# 创建任务表
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL
)
''')

# 提交更改并关闭连接
conn.commit()
conn.close()