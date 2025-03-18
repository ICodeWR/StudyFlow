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

# Module/Script Name: imageStitching.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image

def concatenate_images(image_paths, output_path, direction="horizontal"):
    # 打开所有图像
    images = [Image.open(path) for path in image_paths]

    # 计算拼接后图像的尺寸
    if direction == "horizontal":
        width = sum(im.width for im in images)
        height = max(im.height for im in images)
    else:
        width = max(im.width for im in images)
        height = sum(im.height for im in images)

    # 创建新图像
    new_im = Image.new("RGB", (width, height))

    # 拼接图像
    offset = 0
    for im in images:
        if direction == "horizontal":
            new_im.paste(im, (offset, 0))
            offset += im.width
        else:
            new_im.paste(im, (0, offset))
            offset += im.height

    # 保存图像
    new_im.save(output_path)

# 水平拼接
concatenate_images(['./assets/image1.jpg', "./assets/image2.jpg"], "horizontal.jpg")
# 垂直拼接
concatenate_images(['./assets/image1.jpg', "./assets/image2.jpg"], "vertical.jpg", "vertical")