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

# Module/Script Name: plotly_kline.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day09 exexample Script.

import panel as pn
import plotly.graph_objects as go
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

pn.extension('plotly')

# 获取A股股票数据
def get_stock_data(stock_code):
    # 获取最近180天的数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
    
    try:
        # 获取A股日线数据
        df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date)
        # 重命名列以匹配原始代码
        df = df.rename(columns={
            '日期': 'Date',
            '开盘': 'Open',
            '最高': 'High',
            '最低': 'Low',
            '收盘': 'Close',
            '成交量': 'Volume'
        })


        df['Date'] = pd.to_datetime(df['Date'])
        return df.sort_values('Date')
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None  # 返回None而不是空DataFrame

# 获取A股股票列表
def get_stock_list():
    try:
        print(get_stock_list)
        stock_list = ak.stock_info_a_code_name()
        print(stock_list)
        return stock_list[['code', 'name']].values.tolist()
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return [['000001', '平安银行'], ['600000', '浦发银行']]  # 默认返回一些股票

# 创建控件
stock_list = get_stock_list()
stock_options = {f"{code} {name}": code for code, name in stock_list}

ticker = pn.widgets.AutocompleteInput(
    name='股票代码',
    options=stock_options,
    value='000001',
    placeholder='输入股票代码或名称...'
)

ma_period = pn.widgets.IntSlider(
    name='均线周期',
    start=5, end=60, step=5, value=20
)

volume_toggle = pn.widgets.Toggle(
    name='显示成交量',
    value=True,
    button_type='success'
)

@pn.depends(ticker.param.value, ma_period.param.value, volume_toggle.param.value)
def create_candlestick(stock_code, period, show_volume):
    # 从复合值中提取纯股票代码
    clean_code = stock_code.split(' ')[0] if ' ' in stock_code else stock_code
    df = get_stock_data(clean_code)
    
    # 创建空图表用于错误情况
    fig = go.Figure()
    
    if df is None:
        # 数据获取失败时返回空图表并添加错误信息注释
        fig.add_annotation(
            text="无法获取股票数据，请检查股票代码或网络连接",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        return fig
    
    if df.empty:
        fig.add_annotation(
            text="没有找到数据，请尝试其他股票代码",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        return fig
    
    # 添加K线
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='K线',
        increasing_line_color='red',
        decreasing_line_color='green'
    ))
    
    # 添加均线
    df[f'MA{period}'] = df['Close'].rolling(period).mean()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df[f'MA{period}'],
        line=dict(color='orange', width=2),
        name=f'{period}日均线'
    ))
    
    # 添加成交量
    if show_volume:
        fig.add_trace(go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='成交量',
            marker_color='rgba(100, 100, 100, 0.5)',
            yaxis='y2'
        ))
    
    # 更新布局
    fig.update_layout(
        title=f'{stock_code} 股票走势',
        xaxis_rangeslider_visible=False,
        height=600,
        hovermode='x unified',
        yaxis=dict(title='价格'),
        yaxis2=dict(
            title='成交量',
            overlaying='y',
            side='right',
            showgrid=False
        ) if show_volume else None,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# 创建仪表板
dashboard = pn.Column(
    pn.Row(
        pn.Column(ticker, ma_period, volume_toggle),
        pn.Spacer(width=20)
    ),
    pn.pane.Plotly(create_candlestick, sizing_mode='stretch_width'),
    sizing_mode='stretch_width'
)

# 启动服务
dashboard.servable()

