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

# Module/Script Name: progress_bar_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: Remi day5 exexample Script.


from remi import start, App, gui
import threading
import time

class ProgressBarApp(App):
    def __init__(self, *args):
        super(ProgressBarApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=400, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("实时任务进度条", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建进度条
        self.progress_bar = gui.Progress(width='100%', height=30, style={'margin-bottom': '10px'})
        self.progress_bar.set_value(0)  # 初始值为 0

        # 创建进度标签
        self.progress_label = gui.Label("0%", style={'font-size': '16px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建开始任务按钮
        start_button = gui.Button("开始任务", width=100, height=30)
        start_button.onclick.do(self.on_start_clicked)

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(self.progress_bar)
        root_container.append(self.progress_label)
        root_container.append(start_button)

        # 返回根容器
        return root_container

    def on_start_clicked(self, widget):
        # 禁用按钮，防止重复点击
        widget.set_enabled(False)

        # 启动一个新线程来执行任务
        threading.Thread(target=self.run_task).start()

    def run_task(self):
        # 模拟任务执行过程
        for i in range(101):
            time.sleep(0.1)  # 模拟任务耗时
            self.update_progress(i)

        # 任务完成后启用按钮
        self.progress_label.set_text("任务完成！")
        self.progress_bar.set_value(100)
        self.get_button().set_enabled(True)

    def update_progress(self, value):
        # 更新进度条和标签
        self.progress_bar.set_value(value)
        self.progress_label.set_text(f"{value}%")

    def get_button(self):
        # 获取开始任务按钮
        return self.progress_label.parent.children['start_task_button']

# 启动应用
if __name__ == "__main__":
    start(ProgressBarApp, address='0.0.0.0', port=8080)

