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

# Module/Script Name: imageFilter.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image, ImageFilter

def apply_filter(image_path, output_path, filter_type):
    # 打开图像
    im = Image.open(image_path)

    # 应用滤镜
    if filter_type == "blur":
        filtered = im.filter(ImageFilter.BLUR)
    elif filter_type == "emboss":
        filtered = im.filter(ImageFilter.EMBOSS)
    elif filter_type == "contour":
        filtered = im.filter(ImageFilter.CONTOUR)
    else:
        filtered = im

    # 保存图像
    filtered.save(output_path)

# 应用不同滤镜
apply_filter("./assets/photo.jpg", "blurred.jpg", "blur")
apply_filter("./assets/photo.jpg", "embossed.jpg", "emboss")
apply_filter("./assets/photo.jpg", "contoured.jpg", "contour")