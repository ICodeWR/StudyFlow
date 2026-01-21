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

# Module/Script Name: memory_game.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-06
# Description: NiceGUI exexample Script.

from nicegui import ui
import random
from typing import List, Dict

class MemoryGame:
    def __init__(self):
        self.rows = 4
        self.cols = 4
        self.cards: List[Dict] = []
        self.flipped: List[int] = []
        self.matched: List[int] = []
        self.moves = 0
        self.game_over = False
        self.ui_elements = {}  # 存储UI元素用于更新
        self.game_container = None
        
        # 六一儿童节主题颜色
        self.colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFBE0B',
            '#FB5607', '#8338EC', '#3A86FF', '#FF006E',
            '#A05195', '#D45087', '#F95D6A', '#FF7C43',
            '#FFA600', '#66BD63', '#1A936F', '#114B5F'
        ]
        
        self.init_game()
        
    def init_game(self):
        """初始化游戏"""
        self.cards = []
        self.flipped = []
        self.matched = []
        self.moves = 0
        self.game_over = False
        self.ui_elements.clear()
        
        # 创建卡片对
        symbols = [i for i in range(self.rows * self.cols // 2)] * 2
        random.shuffle(symbols)
        
        for idx, symbol in enumerate(symbols):
            self.cards.append({
                'id': idx,
                'symbol': symbol,
                'color': self.colors[symbol % len(self.colors)],
                'flipped': False,
                'matched': False
            })
        
        self.refresh_ui()
    
    def refresh_ui(self):
        """刷新游戏界面"""
        if self.game_container:
            self.game_container.clear()
            with self.game_container:
                self.create_game_board()
    
    def handle_click(self, card_id: int):
        """处理卡片点击事件"""
        if self.game_over or card_id in self.flipped or card_id in self.matched:
            return
        
        # 如果已经翻开了两张卡片，不做处理
        if len(self.flipped) >= 2:
            return
            
        # 翻开卡片
        self.flipped.append(card_id)
        self.cards[card_id]['flipped'] = True
        self.update_card_ui(card_id)  # 立即更新UI
        
        # 检查是否匹配
        if len(self.flipped) == 2:
            self.moves += 1
            card1 = self.cards[self.flipped[0]]
            card2 = self.cards[self.flipped[1]]
            
            if card1['symbol'] == card2['symbol']:
                # 匹配成功
                self.matched.extend(self.flipped)
                for card_id in self.flipped:
                    self.cards[card_id]['matched'] = True
                    self.update_card_ui(card_id)
                
                # 检查游戏是否结束
                if len(self.matched) == len(self.cards):
                    self.game_over = True
                    ui.notify("🎉 恭喜你赢了！六一儿童节快乐！", type='positive')
                self.flipped.clear()  # 匹配成功时立即清空已翻开的卡片
            else:
                # 不匹配，稍后翻回去
                def flip_back():
                    for card_id in self.flipped:
                        self.cards[card_id]['flipped'] = False
                        self.update_card_ui(card_id)
                    self.flipped.clear()
                ui.timer(1.0, flip_back, once=True)
    
    def update_card_ui(self, card_id: int):
        """更新单个卡片的UI"""
        card = self.cards[card_id]
        if card_id in self.ui_elements:
            front, back, bg, check_icon = self.ui_elements[card_id]
            front.visible = card['flipped'] or card['matched']
            back.visible = not (card['flipped'] or card['matched'])
            bg.style(f"background-color: {card['color']}; opacity: {0.6 if (card['flipped'] or card['matched']) else 0}")
            check_icon.visible = card['matched']
    
    def create_card_ui(self, card: Dict):
        """创建卡片UI"""
        with ui.card().classes('w-24 h-32 items-center justify-center cursor-pointer relative'):
            # 背景色
            bg = ui.element('div').style(f"background-color: {card['color']}; opacity: 0").classes(
                'absolute inset-0 transition-opacity duration-300')
            
            # 卡片正面(显示数字)
            with ui.column().classes('relative z-10 w-full h-full flex items-center justify-center').bind_visibility_from(
                card, 'flipped', lambda x: x or card['matched']) as front:
                ui.label(str(card['symbol'])).classes('text-2xl font-bold text-white')
            
            # 卡片背面(显示问号)
            with ui.column().classes('relative z-10 w-full h-full flex items-center justify-center').bind_visibility_from(
                card, 'flipped', lambda x: not x and not card['matched']) as back:
                ui.icon('question_mark').classes('text-4xl text-gray-600')
            
            # 匹配成功的对勾图标（固定在右下角）
            check_icon = ui.icon('check_circle', size='lg').classes(
                'text-green-500 absolute bottom-1 right-1 z-20').bind_visibility_from(
                card, 'matched')
            
            self.ui_elements[card['id']] = (front, back, bg, check_icon)
            
            # 点击区域
            ui.element('div').on('click', lambda _, cid=card['id']: self.handle_click(cid)).classes(
                'absolute inset-0 z-30')
    
    def create_game_board(self):
        """创建游戏板"""
        with ui.grid(columns=self.cols).classes('gap-2'):
            for card in self.cards:
                self.create_card_ui(card)

# 创建游戏界面
# @ui.page('/')
def create_game_ui():
    """创建游戏界面"""
    game = MemoryGame()
    
    def restart_game():
        """独立的重启游戏函数"""
        game.init_game()
        print("游戏已重启")
        

    with ui.header().classes('bg-blue-100'):
        with ui.row().classes('items-center justify-between w-full'):
            ui.label('🎈 六一儿童节快乐 - 记忆翻牌游戏 🎈').classes('text-xl font-bold text-red-500')
            with ui.row():
                ui.button('重新开始', on_click=restart_game).classes('bg-blue-500 text-white')
                ui.label().bind_text_from(game, 'moves', lambda m: f'步数: {m}').classes('text-lg text-red-700 ml-4')
    
    with ui.row().classes('w-full justify-center p-4') as row:
        game.game_container = row
        game.create_game_board()
    
    # 游戏说明
    with ui.footer().classes('bg-gray-100 p-4'):
        ui.markdown('''
        ### 游戏规则：
        1. 点击卡片翻开它们
        2. 找出所有匹配的卡片对
        3. 用最少的步数完成游戏
        ''').classes('text-sm text-red-500')

# 启动游戏
@ui.page('/')
def main_page():
    create_game_ui()

ui.run(title='六一儿童节记忆游戏', favicon='🎈', dark=False)