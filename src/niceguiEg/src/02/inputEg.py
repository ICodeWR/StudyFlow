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

# Module/Script Name: inputEg.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGui exexample Script.


from nicegui import ui

def submit():
    ui.notify(f'注册成功! 用户名: {username.value}')

with ui.card().classes('w-96 p-4 mx-auto'):
    ui.label('用户注册').classes('text-2xl mb-4')
    
    username = ui.input(
        label='用户名',
        validation={'至少4个字符': lambda v: len(v) >= 4}
    )
    
    password = ui.input(
        label='密码',
        password=True,
        password_toggle_button=True
    )
    
    gender = ui.select(
        ['男', '女', '其他'],
        label='性别'
    )
    
    age = ui.number(
        label='年龄',
        min=1,
        max=120
    )
    
    ui.button('提交', on_click=submit)

ui.run()
