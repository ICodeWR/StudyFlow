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

# Module/Script Name: sales_dashboard.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day03 exexample Script.

import pandas as pd
import numpy as np
import panel  as pn
import plotly.express as px

# 基本初始化（必须在使用交互组件前调用）
pn.extension()

# 创建示例数据
sales_data = pd.DataFrame({
    '日期': pd.date_range('2023-01-01', periods=90),
    '产品线': np.random.choice(['电子产品', '家居用品', '服装', '食品'], 90),
    '地区': np.random.choice(['华东', '华北', '华南', '西部'], 90),
    '销售额': np.random.randint(100, 5000, 90),
    '利润': np.random.randint(10, 500, 90)
})
sales_data['月份'] = sales_data['日期'].dt.month_name()

# 创建控件
time_range = pn.widgets.DateRangeSlider(
    name='日期范围',
    start=sales_data['日期'].min(),
    end=sales_data['日期'].max(),
    value=(sales_data['日期'].min(), sales_data['日期'].max())
)
product_filter = pn.widgets.MultiSelect(
    name='产品线',
    options=list(sales_data['产品线'].unique()),
    value=list(sales_data['产品线'].unique())
)
metric = pn.widgets.Select(name='指标', options=['销售额', '利润'])

# 创建数据视图
@pn.depends(time_range, product_filter, metric)
def create_dashboard(date_range, products, metric):
    # 筛选数据
    filtered = sales_data[
        (sales_data['日期'] >= date_range[0]) & 
        (sales_data['日期'] <= date_range[1]) &
        (sales_data['产品线'].isin(products))
    ]
    
    # 计算汇总指标
    total = filtered[metric].sum()
    avg = filtered[metric].mean()
    
    # 创建图表
    monthly_trend = filtered.groupby('月份')[metric].sum().reset_index()
    trend_fig = px.line(monthly_trend, x='月份', y=metric, title=f'{metric}趋势')
    
    product_dist = filtered.groupby('产品线')[metric].sum().reset_index()
    dist_fig = px.pie(product_dist, names='产品线', values=metric, title='产品分布')
    
    # 创建指标卡
    metrics_row = pn.Row(
        pn.indicators.Number(
            name=f'总{metric}',
            value=total,
            format='￥{value:,.0f}',
            colors=[(total/2, 'red'), (total, 'green')]
        ),
        pn.indicators.Number(
            name=f'平均{metric}',
            value=avg,
            format='￥{value:,.0f}'
        )
    )
    
    # 组合仪表盘
    return pn.Column(
        metrics_row,
        pn.Row(
            pn.pane.Plotly(trend_fig, sizing_mode='stretch_width'),
            pn.pane.Plotly(dist_fig, sizing_mode='stretch_width')
        ),
        pn.widgets.DataFrame(filtered, sizing_mode='stretch_width')
    )

# 完整仪表盘
sales_dashboard = pn.Column(
    pn.Row(
        pn.Column(time_range, product_filter, metric),
        pn.Spacer(width=20)
    ),
    create_dashboard,
    sizing_mode='stretch_width'
)

sales_dashboard.servable('销售分析仪表盘')

