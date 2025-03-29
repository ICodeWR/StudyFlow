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

# Module/Script Name: multi_page_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: Remi day6 exexample Script.

from remi import start, App, gui

class MultiPageApp(App):
    def __init__(self, *args):
        super(MultiPageApp, self).__init__(*args)
        

    def main(self):
        # 创建一个垂直布局容器作为根容器
        self.root_container = gui.VBox(width=400, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})
        self.curr_page = None

        # 创建导航栏
        self.create_navbar()

        # 创建首页
        self.home_page = self.create_home_page()

        # 创建关于页
        self.about_page = self.create_about_page()

        # 创建设置页
        self.settings_page = self.create_settings_page()

        # 默认显示首页
        self.show_page(self.home_page)

        # 返回根容器
        return self.root_container

    def create_navbar(self):
        # 创建一个水平布局容器作为导航栏
        navbar = gui.HBox(width='100%', style={'margin-bottom': '20px'})

        # 创建导航按钮
        home_button = gui.Button("首页", width=80, height=30)
        home_button.onclick.do(lambda widget: self.show_page(self.home_page))

        about_button = gui.Button("关于", width=80, height=30)
        about_button.onclick.do(lambda widget: self.show_page(self.about_page))

        settings_button = gui.Button("设置", width=80, height=30)
        settings_button.onclick.do(lambda widget: self.show_page(self.settings_page))

        # 将按钮添加到导航栏
        navbar.append(home_button)
        navbar.append(about_button)
        navbar.append(settings_button)

        # 将导航栏添加到根容器
        self.root_container.append(navbar)

    def create_home_page(self):
        # 创建一个垂直布局容器作为首页
        home_page = gui.VBox(width='100%', style={'padding': '10px'})

        # 添加欢迎信息
        title = gui.Label("欢迎来到首页！", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})
        home_page.append(title)

        return home_page

    def create_about_page(self):
        # 创建一个垂直布局容器作为关于页
        about_page = gui.VBox(width='100%', style={'padding': '10px'})

        # 添加关于信息
        title = gui.Label("关于我们", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})
        description = gui.Label("这是一个用 Remi 构建的多页面应用示例。", style={'font-size': '16px', 'text-align': 'center'})
        about_page.append(title)
        about_page.append(description)

        return about_page

    def create_settings_page(self):
        # 创建一个垂直布局容器作为设置页
        settings_page = gui.VBox(width='100%', style={'padding': '10px'})

        # 添加设置选项
        title = gui.Label("设置", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})
        option1 = gui.Label("选项 1：启用通知", style={'font-size': '16px', 'margin-bottom': '10px'})
        option2 = gui.Label("选项 2：更改主题", style={'font-size': '16px'})
        settings_page.append(title)
        settings_page.append(option1)
        settings_page.append(option2)

        return settings_page

    def show_page(self, page):
        # 清空根容器的内容（除了导航栏）
        if self.curr_page is not None:
            # print("----curr_page:", self.curr_page)
            # self.curr_page = page
            self.root_container.remove_child(self.curr_page)

        # 显示目标页面
        self.root_container.append(page)
        self.curr_page = page


# 启动应用
if __name__ == "__main__":
    start(MultiPageApp, address='0.0.0.0', port=8080)