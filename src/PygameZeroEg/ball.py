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

# Module/Script Name: ball.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: Pygame Zero exexample Script.

import pgzrun
import random

# 屏幕大小
WIDTH = 800
HEIGHT = 600

# 弹球板
paddle_width = 150
paddle_height = 20
paddle = Rect((WIDTH // 2 - paddle_width // 2, HEIGHT - 50), (paddle_width, paddle_height))
paddle_speed = 5

# 球
ball_radius = 10
ball = Rect((WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius), (ball_radius * 2, ball_radius * 2))
ball_speed_x = 3
ball_speed_y = -3

# 砖块
bricks = []
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 4
BRICK_COLS = WIDTH // BRICK_WIDTH

# 初始化砖块
def create_bricks():
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick = Rect(
                (col * BRICK_WIDTH, row * BRICK_HEIGHT + 50),
                (BRICK_WIDTH - 5, BRICK_HEIGHT - 5)  # 留出间隙
            )
            bricks.append(brick)

create_bricks()

# 更新游戏逻辑
def update():
    global ball_speed_x, ball_speed_y

    # 移动弹球板
    if keyboard.left and paddle.left > 0:
        paddle.x -= paddle_speed
    if keyboard.right and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # 移动球
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # 球碰到边界反弹
    if ball.left < 0 or ball.right > WIDTH:
        ball_speed_x *= -1
    if ball.top < 0:
        ball_speed_y *= -1

    # 球碰到弹球板反弹
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # 球碰到砖块反弹并移除砖块
    for brick in bricks:
        if ball.colliderect(brick):
            ball_speed_y *= -1
            bricks.remove(brick)
            break

    # 球掉到底部，游戏结束
    if ball.top > HEIGHT:
        print("Game Over!")
        reset_game()

    # 所有砖块被击碎，游戏胜利
    if not bricks:
        print("You Win!")
        reset_game()

# 重置游戏
def reset_game():
    global ball, bricks, ball_speed_x, ball_speed_y
    ball.x = WIDTH // 2 - ball_radius
    ball.y = HEIGHT // 2 - ball_radius
    ball_speed_x = 3
    ball_speed_y = -3
    bricks = []
    create_bricks()

# 绘制游戏画面
def draw():
    screen.clear()

    # 绘制弹球板
    screen.draw.filled_rect(paddle, (0, 255, 0))  # 绿色

    # 绘制球
    screen.draw.filled_circle((ball.x + ball_radius, ball.y + ball_radius), ball_radius, (255, 0, 0))  # 红色

    # 绘制砖块
    for brick in bricks:
        screen.draw.filled_rect(brick, (0, 0, 255))  # 蓝色

# 运行游戏
pgzrun.go()