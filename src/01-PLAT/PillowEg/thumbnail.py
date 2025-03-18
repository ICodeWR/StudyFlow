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

# Module/Script Name: thumbnail.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image

def generate_thumbnail(image_path, output_path, size=(100, 100)):
    # 打开图像
    im = Image.open(image_path)

    # 生成缩略图
    im.thumbnail(size)

    # 保存缩略图
    im.save(output_path)

# 批量生成缩略图
images = ["./assets/product1.jpg", "./assets/product2.jpg", "./assets/product3.jpg"]
for i, image in enumerate(images):
    generate_thumbnail(image, f"thumbnail_{i}.jpg")