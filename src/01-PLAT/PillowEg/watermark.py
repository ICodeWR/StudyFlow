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

# Module/Script Name: watermark.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, watermark_text, output_path):
    # 打开图像
    im = Image.open(image_path)

    # 创建绘图对象
    draw = ImageDraw.Draw(im)

    # 加载字体
    # font = ImageFont.truetype("arial.ttf", 160)
    # 加载中文字体（假设字体文件名为“msyh.ttc ”）
    font_path = "C:/Windows/Fonts/msyh.ttc"   # Windows 示例路径
    font = ImageFont.truetype(font_path,  size=160)

    # 添加水印
    draw.text((10, 10), watermark_text, font=font, fill="red")

    # 保存图像
    im.save(output_path)

# 批量添加水印
images = ["./assets/image1.jpg", "./assets/image2.jpg", "./assets/image3.jpg"]
for i, image in enumerate(images):
    add_watermark(image, "@ 水印测试", f"watermarked_{i}.jpg")
    