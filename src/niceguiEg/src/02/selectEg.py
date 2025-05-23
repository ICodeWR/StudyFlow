#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2025 ICodeWR（微信公众号，头条号同名）

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Module/Script Name: inputEg.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGui exexample Script.


from nicegui import ui
from datetime import datetime

# 筛选条件
filters = {
    'status': ui.select(
        ['全部', '待支付', '已发货', '已完成'],
        value='全部',
        label='订单状态'
    ),
    'date_range': ui.select(
        ['全部', '今天', '本周', '本月'],
        value='全部',
        label='时间范围'
    ),
    'category': ui.select( 
        ['电子产品', '服饰', '食品'],
        value=[],
        multiple=True,
        label='商品类别'
    )
}

# 模拟订单数据
orders = [
    {'id': 1, 'status': '待支付', 'date': '2025-05-01', 'category': '电子产品'},
    {'id': 2, 'status': '已发货', 'date': '2025-05-15', 'category': '服饰'},
    {'id': 3, 'status': '已完成', 'date': '2025-05-20', 'category': '食品'}
]

def apply_filters():
    filtered = []
    for order in orders:
        # 状态筛选
        if filters['status'].value != '全部' and order['status'] != filters['status'].value:
            continue
            
        # 时间筛选
        today = datetime.now().date()
        order_date = datetime.strptime(order['date'], '%Y-%m-%d').date()
        
        if filters['date_range'].value == '今天' and order_date != today:
            continue
        elif filters['date_range'].value == '本周' and (today - order_date).days > 7:
            continue
        elif filters['date_range'].value == '本月' and order_date.month != today.month:
            continue
            
        # 类别筛选
        if filters['category'].value and order['category'] not in filters['category'].value:
            continue
            
        filtered.append(order)
    
    # 更新表格
    # table.options['row_data'] = filtered
    table.rows = filtered
    table.update()

# 应用筛选按钮
ui.button('应用筛选', on_click=apply_filters)

# 订单表格
table = ui.table(
    columns = [
        {'headerName': '订单ID', 'field': 'id'},
        {'headerName': '状态', 'field': 'status'},
        {'headerName': '日期', 'field': 'date'},
        {'headerName': '类别', 'field': 'category'}
    ],
    rows = orders
)

ui.run()
