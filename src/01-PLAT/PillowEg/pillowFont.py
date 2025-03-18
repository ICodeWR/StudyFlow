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

# Module/Script Name: pillowFont.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.


from PIL import Image, ImageDraw, ImageFont

# 创建一张空白图片
image = Image.new("RGB",  (400, 200), (255, 255, 255))
draw = ImageDraw.Draw(image)

# 加载中文字体（假设字体文件名为“msyh.ttc ”）
font_path = "C:/Windows/Fonts/msyh.ttc"   # Windows 示例路径
font = ImageFont.truetype(font_path,  size=36)

# 绘制中文文本
draw.text((50,  50), "你好，世界！", font=font, fill=(0, 0, 0))

# 显示或保存图片
image.show() 