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

# Module/Script Name: remi_pandas_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: Remi day10 exexample Script.

from remi import start, App, gui
import pandas as pd

class PandasApp(App):
    def __init__(self, *args):
        super(PandasApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=600, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("数据分析与展示", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建数据表格容器
        self.table = gui.Table(width='100%', height=200, style={'margin-bottom': '20px'})

        # 初始化表头 - 正确的方法
        self.header_row = gui.TableRow()
        
        for text in ['Name', 'Age', 'City']:
            self.header_row.append(gui.TableItem(text))
        self.table.append(self.header_row)


        # 创建统计信息标签
        self.stats_label = gui.Label("统计信息将显示在这里", style={'font-size': '16px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建加载数据按钮
        load_button = gui.Button("加载数据", width=100, height=30)
        load_button.onclick.do(self.on_load_clicked)

        # 创建展示统计信息按钮
        stats_button = gui.Button("展示统计信息", width=150, height=30)
        stats_button.onclick.do(self.on_stats_clicked)

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(self.table)
        root_container.append(self.stats_label)
        root_container.append(load_button)
        root_container.append(stats_button)

        # 返回根容器
        return root_container

    def on_load_clicked(self, widget):
        try:
            # 加载 CSV 数据
            self.df = pd.read_csv('data.csv')
            
            # 清空表格（保留表头）
            keys=[]

            if len(self.table.children) > 1:  # 保留第一行（表头）
                for key, value in self.table.children.items():
                    if value != self.header_row:
                        keys.append(key)
                for key in keys:
                    self.table.remove_child(self.table.children[key])

            # 添加数据行 - 正确的方法
            for _, row in self.df.iterrows():
                table_row = gui.TableRow()
                table_row.append(gui.TableItem(str(row['Name'])))
                table_row.append(gui.TableItem(str(row['Age'])))
                table_row.append(gui.TableItem(str(row['City'])))
                self.table.append(table_row)
        except Exception as e:
            self.stats_label.set_text(f"加载数据失败: {str(e)}")

    def on_stats_clicked(self, widget):
        if hasattr(self, 'df'):
            try:
                # 计算统计信息
                stats = self.df['Age'].describe()
                # 更新统计信息标签
                self.stats_label.set_text(f"统计信息:\n{stats.to_string()}")
            except Exception as e:
                self.stats_label.set_text(f"计算统计信息出错: {str(e)}")
        else:
            self.stats_label.set_text("请先加载数据！")

# 启动 Remi 应用
if __name__ == "__main__":
    start(PandasApp, address='0.0.0.0', port=8080)

