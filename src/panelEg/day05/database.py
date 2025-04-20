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

# Module/Script Name: database.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day05 exexample Script.

import panel  as pn
import pandas as pd
import numpy as np
import sqlite3

# 基本初始化（必须在使用交互组件前调用）
pn.extension()

# 创建模拟数据库
conn = sqlite3.connect(':memory:')
df = pd.DataFrame({
    'id': range(1, 101),
    'product': [f'产品_{i}' for i in range(1, 101)],
    'category': np.random.choice(['电子', '家居', '服装', '食品'], 100),
    'price': np.random.randint(10, 1000, 100)
})
df.to_sql('products', conn, index=False)

# 创建查询组件
category_filter = pn.widgets.Select(name='类别', options=['全部'] + list(df['category'].unique()))
price_range = pn.widgets.RangeSlider(name='价格范围', start=0, end=1000, value=(0, 1000))
search_input = pn.widgets.TextInput(placeholder='搜索产品...')
query_button = pn.widgets.Button(name='查询', button_type='primary')

# 结果表格
result_table = pn.widgets.Tabulator(pagination='remote', page_size=10)

# 异步查询函数
async def run_query(event):
    query_button.loading = True
    try:
        # 构建查询条件
        conditions = []
        params = []
        
        if category_filter.value != '全部':
            conditions.append("category = ?")
            params.append(category_filter.value)
            
        if search_input.value:
            conditions.append("product LIKE ?")
            params.append(f"%{search_input.value}%")
            
        conditions.append("price BETWEEN ? AND ?")
        params.extend(price_range.value)
        
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # 执行查询
        query = f"SELECT * FROM products{where_clause}"
        result_df = pd.read_sql(query, conn, params=params)
        
        # 更新表格
        result_table.value = result_df
        result_table.page = 1  # 重置到第一页
        
    except Exception as e:
        pn.state.notifications.error(f"查询错误: {str(e)}")
    finally:
        query_button.loading = False

# 绑定回调
query_button.on_click(run_query)
category_filter.param.watch(run_query, 'value')
price_range.param.watch(run_query, 'value_throttled')

# 构建界面
dashboard = pn.Column(
    pn.Row(
        pn.Column(
            pn.pane.Markdown("## 产品查询"),
            category_filter,
            price_range,
            search_input,
            query_button,
            width=300
        ),
        pn.Column(
            pn.pane.Markdown("### 查询结果"),
            result_table,
            sizing_mode='stretch_width'
        )
    ),
    sizing_mode='stretch_width'
)

dashboard.servable()

