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

# Module/Script Name: remi_opencv_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: Remi day11 exexample Script.

from remi import start, App, gui
import cv2
import numpy as np
import io
import base64

class OpenCVApp(App):
    def __init__(self, *args):
        super(OpenCVApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=800, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("图像处理与展示", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建图像容器
        self.original_image = gui.Image(width=400, height=300)
        self.processed_image = gui.Image(width=400, height=300)

        # 创建图像容器布局
        image_container = gui.HBox(width='100%', style={'margin-bottom': '20px'})
        image_container.append(self.original_image)
        image_container.append(self.processed_image)

        # 创建按钮容器
        button_container = gui.HBox(width='100%', style={'margin-bottom': '20px'})

        # 创建加载图像按钮
        load_button = gui.Button("加载图像", width=100, height=30)
        load_button.onclick.do(self.on_load_clicked)

        # 创建灰度化按钮
        grayscale_button = gui.Button("灰度化", width=100, height=30)
        grayscale_button.onclick.do(self.on_grayscale_clicked)

        # 创建边缘检测按钮
        edge_button = gui.Button("边缘检测", width=100, height=30)
        edge_button.onclick.do(self.on_edge_clicked)

        # 将按钮添加到容器中
        button_container.append(load_button)
        button_container.append(grayscale_button)
        button_container.append(edge_button)

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(image_container)
        root_container.append(button_container)

        # 返回根容器
        return root_container

    def on_load_clicked(self, widget):
        # 加载图像
        self.image = cv2.imread('image.jpg')
        if self.image is None:
            print("无法加载图像，请检查文件路径")
            return
        # 显示原始图像
        self.show_image(self.image, self.original_image)

    def on_grayscale_clicked(self, widget):
        if hasattr(self, 'image'):
            # 灰度化处理
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 显示处理后的图像
            self.show_image(gray_image, self.processed_image)

    def on_edge_clicked(self, widget):
        if hasattr(self, 'image'):
            # 边缘检测处理
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, 100, 200)

            # 显示处理后的图像
            self.show_image(edges, self.processed_image)

    def show_image(self, image, widget):
        # 对于灰度或边缘检测图像，可能需要转换为3通道
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # 将图像转换为 PNG 格式
        _, buffer = cv2.imencode('.png', image)

        if not _:
            print("图像编码失败")
            return
    
        # 将图像转换为 Base64 编码
        img_str = base64.b64encode(buffer).decode('utf-8')

        # 更新图像组件
        widget.set_image(f"data:image/png;base64,{img_str}")

# 启动 Remi 应用
if __name__ == "__main__":
    start(OpenCVApp, address='0.0.0.0', port=8080)

