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

# Module/Script Name: remi_matplotlib_app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: Remi day09 exexample Script.

import io
import time
import threading
import random

import remi.gui as gui
from remi import start, App

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class MatplotImage(gui.Image):
    ax = None

    def __init__(self, **kwargs):
        super(MatplotImage, self).__init__("/%s/get_image_data?update_index=0" % id(self), **kwargs)
        self._buf = None
        self._buflock = threading.Lock()

        self._fig = Figure(figsize=(4, 4))
        self.ax = self._fig.add_subplot(111)

        self.redraw()

    def redraw(self):
        canv = FigureCanvasAgg(self._fig)
        buf = io.BytesIO()
        canv.print_figure(buf, format='png')
        with self._buflock:
            if self._buf is not None:
                self._buf.close()
            self._buf = buf

        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

        super(MatplotImage, self).redraw()

    def get_image_data(self, update_index):
        with self._buflock:
            if self._buf is None:
                return None
            self._buf.seek(0)
            data = self._buf.read()

        return [data, {'Content-type': 'image/png'}]


class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        wid = gui.VBox(width=320, height=320, margin='0px auto')
        wid.style['text-align'] = 'center'
        
        bt = gui.Button('更新数据', width=100, height=30)
        bt.style['margin'] = '10px'
        bt.onclick.do(self.on_button_pressed)

        self.plot_data = [0, 1]
        self.mpl = MatplotImage(width=250, height=250)
        self.mpl.style['margin'] = '10px'
        self.mpl.ax.set_title("动态数据可视化")
        self.mpl.ax.plot(self.plot_data)
        self.mpl.redraw()

        wid.append(bt)
        wid.append(self.mpl)

        return wid

    def on_button_pressed(self, widget):
        self.plot_data.append(random.random())
        self.mpl.ax.plot(self.plot_data)
        self.mpl.redraw()


if __name__ == "__main__":
    start(MyApp, address='0.0.0.0', port=8080)


