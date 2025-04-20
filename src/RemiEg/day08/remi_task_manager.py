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

# Module/Script Name: remi_task_manager.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: Remi day8 exexample Script.

from remi import start, App, gui
import sqlite3

class TaskManagerApp(App):
    def __init__(self, *args):
        super(TaskManagerApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=400, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("任务管理系统", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建任务列表容器
        self.task_list = gui.VBox(width='100%', style={'margin-bottom': '20px'})

        # 创建添加任务表单
        form_container = gui.VBox(width='100%', style={'margin-bottom': '20px'})
        self.task_input = gui.TextInput(width='100%', height=30, style={'margin-bottom': '10px'})
        add_button = gui.Button("添加任务", width=100, height=30)
        add_button.onclick.do(self.on_add_task_clicked)

        # 将表单组件添加到容器中
        form_container.append(self.task_input)
        form_container.append(add_button)

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(self.task_list)
        root_container.append(form_container)

        # 加载初始任务列表
        self.load_tasks()

        # 返回根容器
        return root_container

    def load_tasks(self):
        # 清空任务列表
        self.task_list.empty()

        # 从数据库获取任务数据
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, text FROM tasks')
        tasks = cursor.fetchall()
        conn.close()

        # 显示任务列表
        for task_id, task_text in tasks:
            task_item = gui.HBox(width='100%', style={'margin-bottom': '10px'})
            task_label = gui.Label(task_text, width='80%', style={'font-size': '16px'})
            delete_button = gui.Button("删除", width=60, height=30)
            delete_button.onclick.do(self.on_delete_task_clicked, task_id)
            task_item.append(task_label)
            task_item.append(delete_button)
            self.task_list.append(task_item)

    def on_add_task_clicked(self, widget):
        # 获取用户输入的任务内容
        task_text = self.task_input.get_value()
        if task_text:
            # 将任务插入数据库
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (text) VALUES (?)', (task_text,))
            conn.commit()
            conn.close()

            # 清空输入框并重新加载任务列表
            self.task_input.set_value('')
            self.load_tasks()

    def on_delete_task_clicked(self, widget, task_id):
        # 从数据库删除任务
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

        # 重新加载任务列表
        self.load_tasks()

# 启动 Remi 应用
if __name__ == "__main__":
    start(TaskManagerApp, address='0.0.0.0', port=8080)
