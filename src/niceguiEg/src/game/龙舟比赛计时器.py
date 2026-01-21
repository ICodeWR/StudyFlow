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

# Module/Script Name: 龙舟比赛计时器.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGUI exexample Script.

from nicegui import ui 
from datetime import datetime, timedelta 
import time 
 
# 端午节主题颜色 (亮色主题)
DRAGON_BOAT_THEME = {
    'primary': '#e74c3c',  # 龙舟红 
    'secondary': '#f1c40f',  # 粽子黄 
    'accent': '#2ecc71',  # 艾草绿 
    'positive': '#27ae60',  # 成功绿 
    'negative': '#e74c3c',  # 警告红 
    'info': '#3498db',  # 信息蓝 
    'warning': '#f39c12',  # 警告橙 
    'background': '#f9f7e8',  # 米色背景 
    'surface': '#ffffff',  # 白色卡片 
    'text': '#2c3e50'  # 深蓝色文字 
}
 
# 初始化队伍数据 
teams = [
    {'name': '青龙队', 'color': '#2ecc71', 'time': None, 'finished': False},
    {'name': '赤龙队', 'color': '#e74c3c', 'time': None, 'finished': False},
    {'name': '黄龙队', 'color': '#f1c40f', 'time': None, 'finished': False},
    {'name': '白龙队', 'color': '#ffffff', 'time': None, 'finished': False},
    {'name': '蓝龙队', 'color': '#3498db', 'time': None, 'finished': False},
]
 
class DragonBoatTimer:
    def __init__(self):
        self.start_time  = None 
        self.is_running  = False 
        self.elapsed_time  = timedelta()
        self.race_distance  = 500  # 500米赛程 
        self.selected_team  = None 
        self.results  = []
        
        # 设置主题 
        ui.colors( 
            primary=DRAGON_BOAT_THEME['primary'],
            secondary=DRAGON_BOAT_THEME['secondary'],
            accent=DRAGON_BOAT_THEME['accent'],
            positive=DRAGON_BOAT_THEME['positive'],
            negative=DRAGON_BOAT_THEME['negative'],
            info=DRAGON_BOAT_THEME['info'],
            warning=DRAGON_BOAT_THEME['warning'],
            background=DRAGON_BOAT_THEME['background'],
            surface=DRAGON_BOAT_THEME['surface'],
            text=DRAGON_BOAT_THEME['text']
        )
        
        self.create_ui() 
        
    def create_ui(self):
        """创建用户界面"""
        with ui.header().style('background-color:  #e74c3c; color: white'):
            with ui.row().classes('items-center'): 
                ui.icon('directions_boat').classes('text-2xl') 
                ui.label(' 端午节龙舟赛计时器').classes('text-2xl font-bold')
        
        with ui.tabs().classes('w-full  bg-amber-50') as tabs:
            self.tab_race  = ui.tab(' 比赛计时')
            self.tab_results  = ui.tab(' 比赛结果')
            self.tab_about  = ui.tab(' 关于端午节')
        
        with ui.tab_panels(tabs,  value=self.tab_race).classes('w-full'): 
            with ui.tab_panel(self.tab_race): 
                self.create_race_ui() 
            with ui.tab_panel(self.tab_results): 
                self.create_results_ui() 
            with ui.tab_panel(self.tab_about): 
                self.create_about_ui() 
    
    def create_race_ui(self):
        """创建比赛计时界面"""
        with ui.row().classes('w-full  justify-center'):
            with ui.card().classes('w-full  items-center').style('background-color: #fffdf6'):
                ui.label(' 端午节龙舟赛').classes('text-2xl font-bold text-red-600')
                ui.image('https://img.zcool.cn/community/01e5e55d554b4ca8012187f4c4d3f9.jpg@1280w_1l_2o_100sh.jpg').classes('w-64') 
                
                with ui.row().classes('w-full  justify-center'):
                    self.timer_display  = ui.label('00:00.000').classes('text-4xl  font-mono text-primary')
                
                with ui.row().classes('w-full  justify-center gap-4'):
                    ui.button(' 开始比赛', on_click=self.start_race,  icon='play_arrow').classes('bg-green-500 text-white')
                    ui.button(' 重置', on_click=self.reset_race,  icon='refresh').classes('bg-red-500 text-white')
                
                ui.separator().classes('bg-amber-200') 
                
                ui.label(' 队伍计时').classes('text-xl font-bold text-amber-700')
                with ui.grid(columns=2).classes('w-full  gap-4'):
                    for i, team in enumerate(teams):
                        with ui.card().classes('shadow-md').style(f'border-left:  4px solid {team["color"]}; background-color: #fffdf6'):
                            with ui.row().classes('items-center'): 
                                ui.label(team['name']).classes('font-bold').style(f'color:  {team["color"]}')
                                team['time_label'] = ui.label(' 未完成').classes('ml-auto text-gray-600')
                            
                            with ui.row().classes('w-full  justify-end'):
                                ui.button(' 到达终点', 
                                         on_click=lambda e, idx=i: self.team_finished(idx), 
                                         icon='flag'
                                        ).classes('bg-amber-500 text-white').bind_visibility_from(teams[i], 'finished', lambda x: not x)
                
                ui.separator().classes('bg-amber-200') 
                ui.label(' 比赛设置').classes('text-xl font-bold text-amber-700')
                with ui.row().classes('w-full  justify-center'):
                    ui.number(' 赛程距离 (米)', 
                             value=self.race_distance,  
                             min=100, 
                             max=1000, 
                             step=50,
                             format='%.0f',
                             on_change=lambda e: setattr(self, 'race_distance', e.value) 
                            ).classes('w-64')
    
    def create_results_ui(self):
        """创建比赛结果界面"""
        with ui.column().classes('w-full  items-center'):
            ui.label(' 比赛结果').classes('text-2xl font-bold text-red-600')
            
            # 使用表格显示结果 
            columns = [
                {'name': 'rank', 'label': '名次', 'field': 'rank', 'align': 'center'},
                {'name': 'team', 'label': '队伍', 'field': 'team', 'align': 'left'},
                {'name': 'time', 'label': '用时', 'field': 'time', 'align': 'center'},
                {'name': 'speed', 'label': '速度 (m/s)', 'field': 'speed', 'align': 'center'},
            ]
            
            self.results_table  = ui.table( 
                columns=columns, 
                rows=[], 
                row_key='rank',
                selection='none'
            ).classes('w-full max-w-2xl').style('background-color: #fffdf6')
            
            ui.button(' 清除结果', 
                     on_click=self.clear_results,  
                     icon='delete'
                    ).classes('bg-red-500 text-white mt-4')
    
    def create_about_ui(self):
        """创建关于端午节的界面"""
        with ui.column().classes('w-full  items-center'):
            ui.label(' 端午节快乐!').classes('text-2xl font-bold text-red-600')
            ui.image('https://img.zcool.cn/community/01b9b35d554b4da801211d53c8d1f7.jpg@1280w_1l_2o_100sh.jpg').classes('w-64') 
            
            with ui.card().classes('w-full  max-w-2xl').style('background-color: #fffdf6'):
                ui.markdown(''' 
                ## 端午节简介 
                
                <span style="color: #e74c3c;">端午节</span>，又称端阳节、龙舟节，是中国传统节日之一，时间为农历五月初五。
                
                ### 传统习俗 
                - 🚣‍ 赛龙舟 
                - 🫔 吃粽子 
                - 🌿 挂艾草与菖蒲 
                - 🧧 佩香囊 
                - 🍶 饮雄黄酒 
                
                ### 节日意义 
                端午节最初是夏季驱离瘟神和祭龙的节日，后来人们将其作为纪念屈原的节日。
                
                <div style="text-align: center; margin-top: 20px;">
                    <span style="color: #e74c3c; font-weight: bold;">祝您端午节安康！</span>
                </div>
                ''').classes('text-lg')
    
    def start_race(self):
        """开始比赛"""
        if not self.is_running: 
            self.start_time  = datetime.now() 
            self.is_running  = True 
            self.update_timer() 
            
            # 重置队伍状态 
            for team in teams:
                team['time'] = None 
                team['finished'] = False 
                team['time_label'].set_text('未完成')
    
    def reset_race(self):
        """重置比赛"""
        self.is_running  = False 
        self.elapsed_time  = timedelta()
        self.timer_display.set_text('00:00.000') 
        
        for team in teams:
            team['time'] = None 
            team['finished'] = False 
            team['time_label'].set_text('未完成')
    
    def update_timer(self):
        """更新计时器显示"""
        if self.is_running: 
            now = datetime.now() 
            elapsed = now - self.start_time  
            self.timer_display.set_text(str(elapsed).split('.')[0]  + '.' + str(elapsed.microseconds  // 1000).zfill(3)[:3])
            ui.timer(0.05,  self.update_timer,  once=True)
    
    def team_finished(self, team_idx):
        """队伍到达终点"""
        if not self.is_running: 
            return 
            
        team = teams[team_idx]
        if not team['finished']:
            finish_time = datetime.now()  - self.start_time  
            team['time'] = finish_time 
            team['finished'] = True 
            team['time_label'].set_text(str(finish_time).split('.')[0] + '.' + str(finish_time.microseconds  // 1000).zfill(3)[:3])
            
            # 计算速度 (m/s)
            speed = self.race_distance  / finish_time.total_seconds() 
            
            # 添加到结果列表 
            self.results.append({ 
                'rank': len(self.results)  + 1,
                'team': team['name'],
                'time': str(finish_time).split('.')[0] + '.' + str(finish_time.microseconds  // 1000).zfill(3)[:3],
                'speed': f'{speed:.2f}',
                'color': team['color']
            })
            
            # 按时间排序 
            self.results.sort(key=lambda  x: datetime.strptime(x['time'],  '%H:%M:%S.%f') if '.' in x['time'] else datetime.strptime(x['time'],  '%H:%M:%S'))
            
            # 更新名次 
            for i, result in enumerate(self.results): 
                result['rank'] = i + 1 
            
            # 更新结果表格 
            self.update_results_table() 
            
            # 检查是否所有队伍都完成了 
            if all(t['finished'] for t in teams):
                self.is_running  = False 
    
    def update_results_table(self):
        """更新结果表格"""
        # 为表格行添加颜色 
        rows = []
        for result in self.results: 
            row = {
                'rank': result['rank'],
                'team': {'label': result['team'], 'style': f'color: {result["color"]}; font-weight: bold'},
                'time': result['time'],
                'speed': result['speed']
            }
            rows.append(row) 
        
        self.results_table.rows  = rows 
        self.results_table.update() 
    
    def clear_results(self):
        """清除比赛结果"""
        self.results  = []
        self.results_table.rows  = []
        self.results_table.update() 
 
# 创建并运行应用 
if __name__ in {"__main__", "__mp_main__"}:
    timer = DragonBoatTimer()
    ui.run(title=' 端午节龙舟赛计时器', favicon='🎏', reload=False)