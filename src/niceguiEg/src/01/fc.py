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

# Module/Script Name: fc.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGui exexample Script.


from nicegui import ui

count = 0

def increment():
    global count
    count += 1
    counter.set_text(f"计数: {count}")

# 页面布局
with ui.column().classes("w-full items-center gap-4"):
    ui.label("简单计数器").classes("text-2xl")
    counter = ui.label(f"计数: {count}")
    ui.button("增加", on_click=increment).classes("w-32")

ui.run(title="我的计数器应用", reload=True)

