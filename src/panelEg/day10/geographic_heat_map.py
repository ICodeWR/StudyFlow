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

# Module/Script Name: geographic_heat_map.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day10 exexample Script.

import altair as alt
import panel as pn
from vega_datasets import data
import pandas as pd

# 初始化Panel
pn.extension('vega')

# 加载机场数据
geo_data = data.airports()

# 创建筛选控件 - 使用机场代码长度作为示例筛选条件
size_range = pn.widgets.RangeSlider(
    name='机场代码长度筛选', 
    start=2, 
    end=4,  # 实际IATA代码通常是3个字母，这里为了演示设为2-4
    value=(2, 3),
    step=1
)

@pn.depends(size_range.param.value)
def create_geo_chart(size_range):
    # 筛选数据：基于机场代码长度
    filtered = geo_data[
        (geo_data['iata'].str.len() >= size_range[0]) & 
        (geo_data['iata'].str.len() <= size_range[1])
    ]
    
    # 创建美国底图
    background = alt.Chart(data.us_10m.url).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        type='albersUsa'
    ).properties(
        width=800,
        height=500,
        title='美国机场分布热力图'
    )
    
    # 创建热力点图层（修正了transform_calculate的位置）
    points = alt.Chart(filtered).mark_circle().transform_calculate(
        iata_length='length(datum.iata)'  # 计算机场代码长度作为热力值
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size('iata_length:Q', 
                     scale=alt.Scale(range=[50, 500]),
                     legend=None),
        color=alt.Color('iata_length:Q', 
                       scale=alt.Scale(scheme='redyellowblue')),
        tooltip=['name:N', 'iata:N', 'city:N', 'state:N']
    )
    
    return (background + points).configure_view(strokeWidth=0)

# 创建仪表盘布局
dashboard = pn.Column(
    pn.pane.Markdown("## 美国机场分布可视化"),
    pn.pane.Markdown("通过机场代码长度筛选并展示分布热力图"),
    size_range,
    pn.pane.Vega(create_geo_chart, sizing_mode='stretch_both')
)

# 显示仪表盘
dashboard.servable()
