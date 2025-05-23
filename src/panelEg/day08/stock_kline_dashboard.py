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

# Module/Script Name: stock_kline_dashboard.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day08 exexample Script.

import panel as pn 
import akshare as ak 
import mplfinance as mpf 
import matplotlib.pyplot  as plt 
from datetime import datetime, timedelta 
from functools import lru_cache 
import pandas as pd 
 
# 设置中文字体 
plt.rcParams['font.sans-serif']  = ['SimHei', 'Microsoft YaHei']  # Windows
plt.rcParams['axes.unicode_minus']  = False  # 修复负号显示

# 初始化设置 
pn.extension() 
 
@lru_cache(maxsize=32)
def get_stock_data(symbol, start_date, end_date):
    try:
        # 获取数据（示例为A股）
        data = ak.stock_zh_a_hist( 
            symbol=symbol[2:] if symbol.startswith(('sh',  'sz')) else symbol,
            period="daily",
            start_date=start_date.strftime("%Y%m%d"), 
            end_date=end_date.strftime("%Y%m%d"), 
            adjust="qfq"
        )
        
        # 列名标准化与索引处理 
        data = data.rename(columns={ 
            '日期': 'Date', '开盘': 'Open', '最高': 'High',
            '最低': 'Low', '收盘': 'Close', '成交量': 'Volume'
        })
        
        if 'Date' not in data.columns:   # 双重验证 
            raise ValueError("数据中缺失Date列")
            
        data['Date'] = pd.to_datetime(data['Date']) 
        data.set_index('Date',  inplace=True)
        return data 
        
    except Exception as e:
        print(f"完整错误信息: {e}")
        return None 
 
def create_error_figure(message):
    fig, ax = plt.subplots(figsize=(10,  6))
    ax.text(0.5,  0.5, message, 
            ha='center', va='center', fontsize=12)
    ax.axis('off') 
    plt.tight_layout() 
    return fig 
 
# 创建交互控件 
symbol = pn.widgets.Select( 
    name='股票代码',
    options={
        '上证指数': 'sh000001', 
        '深证成指': 'sz399001',
        '贵州茅台': 'sh600519',
        '宁德时代': 'sz300750'
    },
    value='sh000001'
)

chart_style = pn.widgets.Select(name=' 图表类型', options=['candle', 'line', 'ohlc', 'renko'])
moving_avg = pn.widgets.IntSlider(name=' 均线周期', start=5, end=50, step=5, value=20)
start_date = pn.widgets.DatePicker(name=' 开始日期', value=datetime.now().date()-timedelta(days=180)) 
end_date = pn.widgets.DatePicker(name=' 结束日期', value=datetime.now().date()) 
volume = pn.widgets.Checkbox(name=' 显示成交量', value=True)
 
@pn.depends(symbol.param.value,  chart_style.param.value,  moving_avg.param.value,  
            start_date.param.value,  end_date.param.value,  volume.param.value) 
def create_kline(ticker, style, ma, start, end, show_volume):
    # 确保所有情况下都返回图形对象 
    data = get_stock_data(ticker, start, end)
    
    if data is None or data.empty: 
        return create_error_figure("没有获取到数据，请检查日期范围或股票代码")
    
    try:
        # 设置mplfinance样式 
        mc = mpf.make_marketcolors( 
            up='red', down='green',
            edge={'up':'red', 'down':'green'},
            wick={'up':'red', 'down':'green'},
            volume='in',
            ohlc='i'
        )
        s = mpf.make_mpf_style( 
            marketcolors=mc, 
            gridstyle='--', 
            gridcolor='lightgray',
            facecolor='white',
            figcolor='white',
            rc={
                'font.family': 'SimHei',  # 指定字体
                'axes.titlesize': 16      # 标题字号
            }
        )
        
        # 添加均线 
        add_plot = [mpf.make_addplot(data['Close'].rolling(ma).mean(), color='blue')]
        
        # 获取股票名称 
        stock_name = dict(symbol.options).get(ticker,  ticker)
        
        fig, _ = mpf.plot( 
            data,
            type=style,
            style=s,
            addplot=add_plot,
            figsize=(12, 7),
            returnfig=True,
            volume=show_volume,
            title=f'{stock_name} K线图',
            warn_too_much_data=len(data)+1 
        )
        plt.close(fig) 
        # 绘制图表
        return fig 
        
    except Exception as e:
        return create_error_figure(f"绘图错误: {str(e)}")
 
# 创建仪表板 
dashboard = pn.Column(
    pn.Row(
        pn.Column(symbol, start_date, end_date),
        pn.Column(chart_style, moving_avg, volume)
    ),
    pn.pane.Matplotlib(create_kline,  dpi=100, sizing_mode='stretch_width')
)
 
dashboard.servable(' 股票K线图分析工具')
