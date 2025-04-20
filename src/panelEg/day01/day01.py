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

# Module/Script Name: day01.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day01 exexample Script.

import panel as pn
import numpy as np
import matplotlib.pyplot as plt

pn.extension()

# 创建控件
frequency = pn.widgets.FloatSlider(name='频率', start=0.1, end=5, step=0.1, value=1)
amplitude = pn.widgets.FloatSlider(name='振幅', start=0.1, end=10, step=0.1, value=1)

# 定义绘图函数
def create_plot(freq, amp):
    x = np.linspace(0, 10, 200)
    y = amp * np.sin(freq * x)
    
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, linewidth=2)
    plt.title(f'y = {amp}·sin({freq}·x)')
    plt.grid(True)
    return plt.gcf()

# 创建交互界面
interactive_plot = pn.bind(create_plot, frequency, amplitude)

dashboard = pn.Column(
    pn.Row(frequency, amplitude),
    interactive_plot,
    sizing_mode='stretch_width'
)

dashboard.servable('正弦波生成器')

