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

# Module/Script Name: alt.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day10 exexample Script.

import pandas as pd
import panel as pn
import altair as alt
import akshare as ak
from datetime import datetime, timedelta

# 启用Panel扩展
pn.extension('vega')

# 获取股票数据函数
def get_stock_data(ticker, start_date, end_date):
    """
    使用AKShare获取股票数据
    参数:
        ticker: 股票代码(如 '000001' 平安银行)
        start_date: 开始日期(格式 'YYYY-MM-DD')
        end_date: 结束日期(格式 'YYYY-MM-DD')
    返回:
        DataFrame包含日期和OHLC数据
    """
    # 转换日期格式
    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    
    try:
        # 获取股票数据
        df = ak.stock_zh_a_hist(symbol=ticker, period="daily", start_date=start_date, end_date=end_date)
        
        # 重命名列以匹配标准OHLC格式
        df = df.rename(columns={
            '日期': 'Date',
            '开盘': 'Open',
            '收盘': 'Close',
            '最高': 'High',
            '最低': 'Low',
            '成交量': 'Volume'
        })
        
        # 转换日期格式
        df['Date'] = pd.to_datetime(df['Date'])
        
        return df.sort_values('Date').reset_index(drop=True)
    except Exception as e:
        print(f"获取数据失败: {e}")
        return pd.DataFrame()

# 创建股票选择控件
ticker_options = {
    '平安银行': '000001',
    '万科A': '000002',
    '宁德时代': '300750',
    '贵州茅台': '600519',
    '中国平安': '601318'
}

ticker = pn.widgets.Select(
    name='选择股票', 
    options=ticker_options,
    value='000001'
)

# 创建日期范围选择器
date_range = pn.widgets.DateRangeSlider(
    name='日期范围',
    start=datetime(2020, 1, 1),
    end=datetime(2023, 1, 1),
    value=(datetime(2020, 1, 1), datetime(2023, 1, 1)),
    step=1
)

# 创建K线图函数
@pn.depends(ticker.param.value, date_range.param.value)
def create_kline_chart(ticker_code, date_range):
    # 获取股票名称
    stock_name = [k for k, v in ticker_options.items() if v == ticker_code][0]
    
    # 转换日期格式
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
    
    # 获取数据
    df = get_stock_data(ticker_code, start_date, end_date)
    
    if df.empty:
        return pn.pane.Alert("无法获取数据，请检查股票代码或日期范围", alert_type="danger")
    
    # 创建基础图表
    base = alt.Chart(df).encode(
        x='Date:T',
        tooltip=['Date:T', 'Open:Q', 'High:Q', 'Low:Q', 'Close:Q', 'Volume:Q']
    ).properties(
        title=f'{stock_name}({ticker_code}) K线图',
        width=800,
        height=400
    )
    
    # 创建K线图的规则(高低线)
    rule = base.mark_rule().encode(
        y='Low:Q',
        y2='High:Q',
        color=alt.value('#333333')
    )

    # 创建K线图的柱体(开盘收盘)
    bar = base.mark_bar().encode(
        y='Open:Q',
        y2='Close:Q',
        color=alt.condition(
            "datum.Open <= datum.Close",
            alt.value("#06982d"),  # 上涨颜色
            alt.value("#ae1325")    # 下跌颜色
        )
    )
    
    # 组合K线图
    kline_chart = (rule + bar).interactive()
    
    # 创建成交量图表
    volume_chart = alt.Chart(df).mark_bar().encode(
        x='Date:T',
        y='Volume:Q',
        color=alt.condition(
            "datum.Open <= datum.Close",
            alt.value("#06982d"),  # 上涨颜色
            alt.value("#ae1325")   # 下跌颜色
        ),
        tooltip=['Date:T', 'Volume:Q']
    ).properties(
        width=800,
        height=150
    ).interactive()
    
    # 组合图表
    combined_chart = alt.vconcat(
        kline_chart,
        volume_chart,
        spacing=10
    ).resolve_scale(
        x='shared'
    )
    
    return combined_chart

# 创建移动平均线分析函数
@pn.depends(ticker.param.value, date_range.param.value)
def create_ma_chart(ticker_code, date_range):
    # 获取股票名称
    stock_name = [k for k, v in ticker_options.items() if v == ticker_code][0]
    
    # 转换日期格式
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
    
    # 获取数据
    df = get_stock_data(ticker_code, start_date, end_date)
    
    if df.empty:
        return pn.pane.Alert("无法获取数据，请检查股票代码或日期范围", alert_type="danger")
    
    # 计算移动平均
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    
    # 创建基础图表
    base = alt.Chart(df).encode(
        x='Date:T',
        y='Close:Q',
        tooltip=['Date:T', 'Close:Q', 'MA5:Q', 'MA10:Q', 'MA20:Q']
    ).properties(
        title=f'{stock_name}({ticker_code}) 移动平均线',
        width=800,
        height=400
    )
    
    # 创建收盘价线
    price_line = base.mark_line(color='black').encode(
        y='Close:Q'
    )
    
    # 创建移动平均线
    ma5_line = base.mark_line(color='blue').encode(
        y='MA5:Q'
    )
    
    ma10_line = base.mark_line(color='orange').encode(
        y='MA10:Q'
    )
    
    ma20_line = base.mark_line(color='green').encode(
        y='MA20:Q'
    )
    
    # 组合图表
    ma_chart = (price_line + ma5_line + ma10_line + ma20_line).interactive()
    
    return ma_chart

# 创建仪表板布局
dashboard = pn.Column(
    pn.Row(
        pn.Column(
            pn.pane.Markdown("<h2 style='font-size:20px'>股票数据分析仪表板</h2>"),
            ticker,
            date_range,
            pn.pane.Markdown("使用AKShare数据源，Panel构建界面，Altair可视化"),
            width=300
        ),
        pn.Tabs(
            ('K线图', pn.pane.Vega(create_kline_chart, height=600)),
            ('移动平均线', pn.pane.Vega(create_ma_chart, height=600)),
        )
    )
)

# 显示仪表板
dashboard.servable()
