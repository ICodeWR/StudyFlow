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

# Module/Script Name: imageDataAugmentation.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image, ImageEnhance, ImageOps
import os

def augment_image(image_path, output_folder):
    # 打开图像
    im = Image.open(image_path)

    # 增强亮度
    enhancer = ImageEnhance.Brightness(im)
    brightened = enhancer.enhance(1.5)
    brightened.save(os.path.join(output_folder, "brightened.jpg"))

    # 增强对比度
    enhancer = ImageEnhance.Contrast(im)
    contrasted = enhancer.enhance(2.0)
    contrasted.save(os.path.join(output_folder, "contrasted.jpg"))

    # 水平翻转
    flipped = im.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save(os.path.join(output_folder, "flipped.jpg"))

# 批量增强数据
augment_image("./assets/dataset_image.jpg", "augmented_data")