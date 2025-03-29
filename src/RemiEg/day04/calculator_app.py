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

# Module/Script Name: calculator_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: Remi day04 exexample Script.

from remi import start, App, gui

class CalculatorApp(App):
    def __init__(self, *args):
        super(CalculatorApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=300, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("动态计算器", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建输入框容器
        input_container = gui.VBox(width='100%', style={'margin-bottom': '20px'})

        # 创建第一个输入框
        self.num1_input = gui.TextInput(width='100%', height=30, style={'margin-bottom': '10px'})
        self.num1_input.attributes['placeholder'] = '输入第一个数字'  # 设置占位符

        # 创建第二个输入框
        self.num2_input = gui.TextInput(width='100%', height=30, style={'margin-bottom': '20px'})
        self.num2_input.attributes['placeholder'] = '输入第二个数字'  # 设置占位符

        # 将输入框添加到容器中
        input_container.append(self.num1_input)
        input_container.append(self.num2_input)

        # 创建按钮容器
        button_container = gui.HBox(width='100%', style={'margin-bottom': '20px'})

        # 创建加、减、乘、除按钮
        add_button = gui.Button("+", width=50, height=30)
        add_button.onclick.do(self.on_add_clicked)

        subtract_button = gui.Button("-", width=50, height=30)
        subtract_button.onclick.do(self.on_subtract_clicked)

        multiply_button = gui.Button("×", width=50, height=30)
        multiply_button.onclick.do(self.on_multiply_clicked)

        divide_button = gui.Button("÷", width=50, height=30)
        divide_button.onclick.do(self.on_divide_clicked)

        # 将按钮添加到容器中
        button_container.append(add_button)
        button_container.append(subtract_button)
        button_container.append(multiply_button)
        button_container.append(divide_button)

        # 创建结果显示标签
        self.result_label = gui.Label("结果将显示在这里", style={'font-size': '16px', 'text-align': 'center'})

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(input_container)
        root_container.append(button_container)
        root_container.append(self.result_label)

        # 返回根容器
        return root_container

    def on_add_clicked(self, widget):
        self.calculate("add")

    def on_subtract_clicked(self, widget):
        self.calculate("subtract")

    def on_multiply_clicked(self, widget):
        self.calculate("multiply")

    def on_divide_clicked(self, widget):
        self.calculate("divide")

    def calculate(self, operation):
        try:
            # 获取用户输入
            num1 = float(self.num1_input.get_value())
            num2 = float(self.num2_input.get_value())

            # 根据操作符计算结果
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                result = num1 / num2 if num2 != 0 else "错误：除数不能为0"

            # 显示结果
            self.result_label.set_text(f"结果: {result}")
        except ValueError:
            self.result_label.set_text("错误：请输入有效的数字")

# 启动应用
if __name__ == "__main__":
    start(CalculatorApp, address='0.0.0.0', port=8080)