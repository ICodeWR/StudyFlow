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

# Module/Script Name: imageCropRotate.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-03
# Description: Pillow exexample Script.

from PIL import Image

def crop_and_rotate(image_path, output_path, crop_box, rotate_angle):
    # 打开图像
    im = Image.open(image_path)

    # 裁剪图像
    cropped = im.crop(crop_box)

    # 旋转图像
    rotated = cropped.rotate(rotate_angle)

    # 保存图像
    rotated.save(output_path)

# 裁剪并旋转图像
crop_and_rotate("./assets/photo.jpg", "cropped_rotated.jpg", (100, 100, 400, 400), 45)