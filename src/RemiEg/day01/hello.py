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

# Module/Script Name: hello.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Remi exexample Script.

from remi import start, App, gui

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # 创建一个容器
        container = gui.VBox(width=300, height=200, style={'margin': 'auto'})

        # 创建一个标签，显示 "Hello, World!"
        label = gui.Label("Hello, World!", style={'font-size': '20px', 'text-align': 'center'})

        # 将标签添加到容器中
        container.append(label)

        # 返回容器作为应用的根元素
        return container

# 启动应用
if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8080)

