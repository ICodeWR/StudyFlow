#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2025 ICodeWR（微信公众号，头条号同名）

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Module/Script Name: login_app2.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Remi exexample Script.

from remi import start, App, gui

class LoginApp(App):
    def __init__(self, *args):
        super(LoginApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器
        container = gui.VBox(width=300, height=200, style={'margin': 'auto', 'padding': '20px'})

        # 创建一个标题标签
        title = gui.Label("用户登录", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建用户名输入框
        username_label = gui.Label("用户名:", style={'font-size': '16px'})
        self.username_input = gui.TextInput(width=200, height=30, style={'margin-bottom': '10px'})

        # 创建密码输入框
        password_label = gui.Label("密码:", style={'font-size': '16px'})
        self.password_input = gui.Input(width=200, height=30, style={'margin-bottom': '10px'}, input_type='password')


        # 创建登录按钮
        login_button = gui.Button("登录", width=100, height=30)
        login_button.onclick.do(self.on_login_clicked)  # 绑定点击事件

        # 创建结果显示标签
        self.result_label = gui.Label("", style={'font-size': '16px', 'text-align': 'center'})

        # 将组件添加到容器中
        container.append(title)
        container.append(username_label)
        container.append(self.username_input)
        container.append(password_label)
        container.append(self.password_input)
        container.append(login_button)
        container.append(self.result_label)

        # 返回容器作为应用的根元素
        return container

    def on_login_clicked(self, widget):
        # 获取用户名和密码
        username = self.username_input.get_value()
        password = self.password_input.get_value()

        # 显示结果
        self.result_label.set_text(f"用户名: {username}, 密码: {password}")

# 启动应用
if __name__ == "__main__":
    start(LoginApp, address='0.0.0.0', port=8080)


