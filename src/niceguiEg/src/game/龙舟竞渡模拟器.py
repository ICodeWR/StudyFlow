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

# Module/Script Name: 龙舟竞渡模拟器.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGUI exexample Script.

from nicegui import ui
import random 
import time
from datetime import datetime 
import plotly.graph_objects  as go
 
class DragonBoatRacePlotly:
    def __init__(self):
        self.version  = "1.0.0"
        self.title  = "端午龙舟竞渡模拟器 (Plotly版)"
        self.player_name  = "选手"
        self.game_started  = False 
        self.race_finished  = False
        self.boats  = []
        self.start_time  = None 
        self.setup_ui() 
        
    def setup_ui(self):
        """初始化用户界面"""
        ui.colors(primary='#D32F2F',  secondary='#F44336', accent='#FF5722')
        
        with ui.header().classes('bg-red-8  text-white justify-between'):
            ui.label(f'🏮  {self.title}  v{self.version}').classes('text-2xl') 
            ui.button(' 关于', on_click=self.show_about).props('flat') 
        
        with ui.tabs().classes('w-full')  as tabs:
            self.tab_home  = ui.tab(' 首页')
            self.tab_game  = ui.tab(' 比赛')
            self.tab_records  = ui.tab(' 记录')
        
        self.tab_panels  = ui.tab_panels(tabs,  value=self.tab_home).classes('w-full') 
        with self.tab_panels: 
            with ui.tab_panel(self.tab_home): 
                self.create_home_tab() 
            with ui.tab_panel(self.tab_game): 
                self.create_game_tab() 
            with ui.tab_panel(self.tab_records): 
                self.create_records_tab() 
    
    def create_home_tab(self):
        """创建首页内容"""
        with ui.column().classes('items-center  gap-4'):
            ui.label('🏮  端午龙舟竞渡模拟器 🏮').classes('text-h4 text-weight-bold text-red-10')
            ui.image('https://img.zcool.cn/community/01e5b55d15c5cda8012187f4d4e1b4.jpg').classes('w-64') 
            
            with ui.card().classes('w-full  max-w-2xl'):
                ui.label(' 端午节介绍').classes('text-h5')
                ui.markdown(''' 
                端午节，又称端阳节、龙舟节，是中国传统节日之一。  
                赛龙舟是端午节的重要习俗，起源于古代楚国人纪念屈原的活动。  
                本模拟器让你体验龙舟竞渡的乐趣！
                ''')
            
            self.player_name_input  = ui.input(' 你的名字', value=self.player_name) 
            
            with ui.row().classes('gap-4'): 
                ui.button(' 开始单人比赛', on_click=lambda: self.start_game(False)).classes('bg-positive') 
                ui.button(' 开始多人比赛', on_click=lambda: self.start_game(True)).classes('bg-primary') 
    
    def create_game_tab(self):
        """创建比赛页面"""
        with ui.column().classes('items-center  w-full'):
            self.game_status  = ui.label(' 准备开始比赛...').classes('text-h5')
            
            # 创建Plotly图表容器
            self.fig  = self.create_initial_plot() 
            self.plotly_container  = ui.plotly(self.fig).classes('w-full  h-96')
            
            with ui.row().classes('gap-4'): 
                self.paddle_button  = ui.button(' 划桨', on_click=self.paddle).props('disabled') 
                ui.button(' 重新开始', on_click=self.reset_game).classes('bg-warning') 
                ui.button(' 返回首页', on_click=lambda: self.tab_panels.set_value(self.tab_home)) 
    
    def create_records_tab(self):
        """创建记录页面"""
        with ui.column().classes('items-center  w-full'):
            ui.label(' 比赛记录').classes('text-h4')
            
            columns = [
                {'name': 'date', 'label': '日期', 'field': 'date'},
                {'name': 'player', 'label': '选手', 'field': 'player'},
                {'name': 'result', 'label': '成绩', 'field': 'result'},
                {'name': 'time', 'label': '用时', 'field': 'time'}
            ]
            self.records  = []
            
            self.records_table  = ui.table(columns=columns,  rows=self.records).classes('w-full  max-w-2xl')
    
    def create_initial_plot(self):
        """创建初始Plotly图表"""
        fig = go.Figure()
        
        # 设置图表布局 
        fig.update_layout( 
            title='端午龙舟竞渡',
            xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=[0, 60], showgrid=False, zeroline=False, visible=False),
            plot_bgcolor='rgba(30, 136, 229, 0.3)',
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False,
            shapes=[
                dict(
                    type='line',
                    x0=100, y0=0,
                    x1=100, y1=60,
                    line=dict(color='black', width=3, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x=100, y=62,
                    text='终点',
                    showarrow=False,
                    font=dict(size=14)
                )
            ]
        )
        
        return fig 
    
    def draw_boats(self):
        """绘制龙舟"""
        self.fig.data  = []  # 清除之前的龙舟轨迹 
        
        # 绘制每条龙舟 
        for i, boat in enumerate(self.boats): 
            color = 'red' if i == 0 else 'orange'
            
            # 龙舟主体 (三角形)
            x_points = [boat['x'], boat['x'] + 15, boat['x'] + 15, boat['x']]
            y_points = [boat['y'], boat['y'] + 5, boat['y'] - 5, boat['y']]
            
            self.fig.add_trace(go.Scatter( 
                x=x_points,
                y=y_points,
                fill='toself',
                fillcolor=color,
                line=dict(color='black', width=1),
                mode='lines',
                name=boat['name']
            ))
            
            # 龙头 (三角形)
            x_head = [boat['x'] + 15, boat['x'] + 20, boat['x'] + 20, boat['x'] + 15]
            y_head = [boat['y'] + 5, boat['y'] + 8, boat['y'] - 8, boat['y'] - 5]
            
            self.fig.add_trace(go.Scatter( 
                x=x_head,
                y=y_head,
                fill='toself',
                fillcolor='brown',
                line=dict(color='black', width=1),
                mode='lines'
            ))
            
            # 选手名字
            self.fig.add_annotation( 
                x=boat['x'] + 7,
                y=boat['y'] + 8,
                text=boat['name'],
                showarrow=False,
                font=dict(size=12, color='black')
            )
        
        # 更新图表显示 
        self.plotly_container.update() 
    
    def start_game(self, multiplayer: bool):
        """开始游戏"""
        self.player_name  = self.player_name_input.value  or "选手"
        self.game_started  = True
        self.race_finished  = False 
        self.start_time  = time.time() 
        self.tab_panels.set_value(self.tab_game) 
        
        # 初始化龙舟 
        self.boats  = [{'x': 10, 'y': 30, 'speed': 0, 'name': self.player_name}] 
        if multiplayer:
            self.boats.extend([ 
                {'x': 10, 'y': 20, 'speed': 0, 'name': '龙舟队A'},
                {'x': 10, 'y': 40, 'speed': 0, 'name': '龙舟队B'}
            ])
        
        self.paddle_button.props(remove='disabled') 
        self.game_status.set_text(' 比赛开始！用力划桨！')
        self.draw_boats() 
        
        # AI对手自动划桨
        if multiplayer:
            self.ai_timer  = ui.timer(0.5,  self.ai_paddle) 
    
    def paddle(self):
        """玩家划桨"""
        if not self.game_started  or self.race_finished: 
            return 
        
        # 玩家龙舟加速 
        self.boats[0]['speed']  += random.uniform(1.0,  3.0)
        self.update_race() 
    
    def ai_paddle(self):
        """AI对手划桨"""
        if not self.game_started  or self.race_finished: 
            return
        
        for boat in self.boats[1:]: 
            boat['speed'] += random.uniform(0.8,  2.5)
        self.update_race() 
    
    def update_race(self):
        """更新比赛状态"""
        if self.race_finished: 
            return
        
        # 更新龙舟位置
        for boat in self.boats: 
            boat['x'] += boat['speed']
            boat['speed'] *= 0.95  # 速度衰减
        
        # 检查是否到达终点
        finished = [b for b in self.boats  if b['x'] >= 100]
        if finished:
            self.race_finished  = True 
            winner = min(finished, key=lambda b: b['x'] - 100)
            elapsed_time = time.time()  - self.start_time 
            self.game_status.set_text(f' 比赛结束！{winner["name"]}获胜！用时: {elapsed_time:.1f}秒')
            
            # 记录比赛结果 
            self.add_record( 
                player=self.player_name, 
                result='冠军' if winner == self.boats[0]  else '参与',
                time=f'{elapsed_time:.1f}秒'
            )
            
            self.paddle_button.props('disabled') 
            if hasattr(self, 'ai_timer'):
                self.ai_timer.deactivate() 
        
        self.draw_boats() 
    
    def add_record(self, player: str, result: str, time: str):
        """添加比赛记录"""
        self.records.append({ 
            'date': datetime.now().strftime('%Y-%m-%d'), 
            'player': player,
            'result': result,
            'time': time
        })
        self.records_table.update() 
    
    def reset_game(self):
        """重置游戏"""
        self.game_started  = False 
        self.race_finished  = False
        if hasattr(self, 'ai_timer'):
            self.ai_timer.deactivate() 
        
        self.paddle_button.props('disabled') 
        self.game_status.set_text(' 准备开始比赛...')
        self.fig  = self.create_initial_plot() 
        self.plotly_container.update() 
    
    def show_about(self):
        """显示关于信息"""
        with ui.dialog()  as dialog, ui.card(): 
            ui.label(' 关于端午龙舟竞渡模拟器').classes('text-h5')
            ui.markdown(f''' 
            **版本**: {self.version}   
            **作者**: NiceGUI开发者  
            **描述**: 一个模拟端午节龙舟比赛的小游戏  
            
            使用NiceGUI {ui.version} 和Plotly构建
            ''')
            ui.button(' 关闭', on_click=dialog.close) 
        dialog.open() 
 
# 启动应用 
app = DragonBoatRacePlotly()
ui.run(title=app.title,  favicon="🎏", dark=True)