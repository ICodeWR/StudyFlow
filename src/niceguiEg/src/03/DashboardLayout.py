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

# Module/Script Name: DashboardLayout.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGUI exexample Script.

from nicegui import ui
from datetime import datetime 
import random
 
# 模拟数据 
def generate_metrics():
    return {
        'visitors': random.randint(1000,  5000),
        'conversion': random.uniform(0.1,  0.5),
        'revenue': random.randint(5000,  20000),
        'orders': random.randint(50,  300)
    }
 
# 自定义 metric 组件
def metric(title: str, value: str):
    with ui.card().classes('shadow  p-4 text-center'):
        ui.label(title).classes('text-sm  text-gray-500')
        ui.label(value).classes('text-2xl  font-bold')
 
# 创建响应式仪表盘
def create_dashboard():
    # 顶部状态栏
    with ui.header().classes(''' 
        grid grid-cols-4 gap-4
        sm:grid-cols-2 sm:gap-2
        lg:grid-cols-4 
        p-4 bg-blue-50
    '''):
        metrics = generate_metrics()
        metric('访客', f'{metrics["visitors"]:,}')
        metric('转化率', f'{metrics["conversion"]:.1%}')
        metric('收入', f'¥{metrics["revenue"]:,}')
        metric('订单', str(metrics["orders"]))
 
    # 主内容区 
    with ui.grid(columns='300px  1fr').classes('gap-4 h-[calc(100vh-120px)]'):
        # 左侧导航
        with ui.column().classes(''' 
            bg-gray-50 p-4 
            hidden sm:flex  # 移动端隐藏 
        '''):
            ui.label(' 导航菜单').classes('text-lg font-bold mb-4')
            for item in ['概览', '分析', '报表', '设置']:
                ui.button(item).props('flat').classes('justify-start') 
        
        # 右侧内容 
        with ui.grid(rows='auto  1fr').classes('gap-4 w-full'):
            # 选项卡
            with ui.tabs()  as tabs:
                ui.tab(' 实时数据')
                ui.tab(' 趋势分析')
                ui.tab(' 用户画像')
            
            with ui.tab_panels(tabs,  value='实时数据').classes('w-full h-full'):
                # 面板1: 实时数据 
                with ui.tab_panel(' 实时数据'):
                    create_realtime_panel()
                
                # 面板2: 趋势分析
                with ui.tab_panel(' 趋势分析'):
                    create_trend_panel()
                
                # 面板3: 用户画像 
                with ui.tab_panel(' 用户画像'):
                    create_user_panel()
 
def create_realtime_panel():
    with ui.grid(columns='2fr  1fr').classes('gap-4 h-full'):
        # 主图表区 
        with ui.card().classes('col-span-2  lg:col-span-1'):
            ui.label(' 实时流量').classes('text-lg')
            ui.echart({ 
                'xAxis': {'type': 'category', 'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']},
                'yAxis': {'type': 'value'},
                'series': [{'data': [120, 200, 150, 80, 70], 'type': 'line'}]
            })
        
        # 侧边栏 
        with ui.column().classes('gap-4'): 
            with ui.card().classes('h-1/2'): 
                ui.label(' 最新动态')
            with ui.card().classes('h-1/2'): 
                ui.label(' 热门内容')
 
def create_trend_panel():
    with ui.grid(columns=2).classes('gap-4  h-full'):
        for i in range(4):
            with ui.card(): 
                ui.label(f' 趋势图{i+1}').classes('text-lg')
                # 使用 ui.echart()  替代 ui.line_chart() 
                data = [(x, x**2) for x in range(10)]
                ui.echart({ 
                    'xAxis': {'type': 'value'},
                    'yAxis': {'type': 'value'},
                    'series': [{
                        'data': data,
                        'type': 'line',
                        'smooth': True
                    }]
                })
 
def create_user_panel():
    with ui.grid(columns='repeat(auto-fit,  minmax(200px, 1fr))').classes('gap-4'):
        for i in range(6):
            with ui.card(): 
                ui.avatar(f'U{i+1}',  size='lg')
                ui.label(f' 用户组{i+1}').classes('text-center')
 
# 初始化仪表盘
create_dashboard()
 
# 响应式控制
ui.button(' 切换移动视图', on_click=lambda: ui.run_javascript(''' 
    const viewport = document.querySelector('meta[name="viewport"]'); 
    viewport.content  = viewport.content.includes('width=400')  ? 
        'width=device-width' : 'width=400';
''')) 
 
ui.run() 