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

# Module/Script Name: smart_home.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day06 exexample Script.

import panel  as pn
import param

class SmartHome(param.Parameterized):
    lighting = param.Number(0, bounds=(0, 100), doc="灯光亮度")
    temperature = param.Number(22.0, bounds=(10, 30), doc="目标温度")
    security = param.Boolean(False, doc="安防模式")
    
    @param.depends('lighting')
    def light_control(self):
        color = '#FFF3B0' if self.lighting > 0 else '#4A4A4A'
        return pn.indicators.Gauge(
            name='灯光',
            value=self.lighting,
            bounds=(0, 100),
            colors=[(self.lighting/100, color)],
            format='{value}%'
        )
    
    @param.depends('temperature')
    def temp_view(self):
        return pn.indicators.LinearGauge(
            value=self.temperature,
            bounds=(10, 30),
            colors=[(0.3, 'blue'), (0.7, 'green'), (1, 'red')]
        )
    
    @param.depends('security')
    def security_view(self):
        status = "启动" if self.security else "关闭"
        return pn.pane.Alert(
            f"安防系统: {status}",
            alert_type="warning" if self.security else "success"
        )
    
    def control_panel(self):
        return pn.Column(
            pn.Param(
                self.param,
                widgets={
                    'lighting': {'type': pn.widgets.IntSlider},
                    'temperature': {'type': pn.widgets.FloatSlider},
                    'security': {'type': pn.widgets.Toggle}
                }
            ),
            self.light_control,
            self.temp_view,
            self.security_view
        )

smart_home = SmartHome()
smart_home.control_panel().servable()



