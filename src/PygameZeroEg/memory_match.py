#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Module/Script Name: memory_match.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: Pygame Zero exexample Script.

import pygame
import random
import time
import os

# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("六一儿童节快乐 - 记忆翻牌游戏")

# 尝试加载中文字体（使用系统自带字体或指定路径）
try:
    # Windows系统常见中文字体路径
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simkai.ttf",  # 楷体
        "C:/Windows/Fonts/simsun.ttc",  # 宋体
        "/System/Library/Fonts/STHeiti Medium.ttc",  # Mac系统黑体
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  # Linux文泉驿微米黑
    ]
    
    # 找到第一个可用的字体
    chinese_font = None
    for path in font_paths:
        if os.path.exists(path):
            chinese_font = pygame.font.Font(path, 36)
            break
    
    # 如果没有找到系统字体，使用默认字体（可能不支持中文）
    if chinese_font is None:
        chinese_font = pygame.font.SysFont(None, 36)
except:
    chinese_font = pygame.font.SysFont(None, 36)

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLORS = [BLUE, GREEN, RED, (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# 游戏参数
ROWS, COLS = 4, 4
CARD_WIDTH = WIDTH // COLS - 10
CARD_HEIGHT = HEIGHT // ROWS - 10
CARD_MARGIN = 5

# 创建卡片
def create_board():
    symbols = []
    for i in range(ROWS * COLS // 2):
        symbols.append(i)
        symbols.append(i)
    random.shuffle(symbols)
    
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            symbol = symbols.pop()
            board_row.append({
                'symbol': symbol,
                'color': COLORS[symbol % len(COLORS)],
                'flipped': False,
                'matched': False
            })
        board.append(board_row)
    return board

# 绘制卡片
def draw_board(board):
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            card = board[row][col]
            rect = pygame.Rect(
                col * (CARD_WIDTH + CARD_MARGIN) + CARD_MARGIN,
                row * (CARD_HEIGHT + CARD_MARGIN) + CARD_MARGIN,
                CARD_WIDTH,
                CARD_HEIGHT
            )
            
            if card['flipped'] or card['matched']:
                pygame.draw.rect(screen, card['color'], rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                text = chinese_font.render(str(card['symbol']), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, (200, 200, 200), rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
    
    pygame.display.flip()

# 显示中文消息
def show_message(message, color, duration=2000):
    screen.fill(WHITE)
    text = chinese_font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(duration)

# 主游戏循环
def main():
    board = create_board()
    flipped_cards = []
    matched_pairs = 0
    total_pairs = ROWS * COLS // 2
    
    running = True
    show_message("六一儿童节快乐！", RED, 1500)
    show_message("点击卡片开始游戏", BLUE, 1500)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (CARD_WIDTH + CARD_MARGIN)
                row = pos[1] // (CARD_HEIGHT + CARD_MARGIN)
                
                if 0 <= row < ROWS and 0 <= col < COLS:
                    card = board[row][col]
                    if not card['flipped'] and not card['matched'] and len(flipped_cards) < 2:
                        card['flipped'] = True
                        flipped_cards.append((row, col))
        
        # 检查是否翻开了两张卡片
        if len(flipped_cards) == 2:
            draw_board(board)
            pygame.time.delay(500)  # 短暂延迟以便玩家看到
            
            (row1, col1), (row2, col2) = flipped_cards
            card1 = board[row1][col1]
            card2 = board[row2][col2]
            
            if card1['symbol'] == card2['symbol']:
                card1['matched'] = True
                card2['matched'] = True
                matched_pairs += 1
                
                # 检查游戏是否结束
                if matched_pairs == total_pairs:
                    show_message("恭喜你赢了！", RED)
                    board = create_board()
                    flipped_cards = []
                    matched_pairs = 0
            else:
                card1['flipped'] = False
                card2['flipped'] = False
            
            flipped_cards = []
        
        draw_board(board)
    
    pygame.quit()

if __name__ == "__main__":
    main()