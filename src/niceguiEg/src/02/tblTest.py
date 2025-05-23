from nicegui import ui

# 列定义
columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'required': True},
    {'name': 'name', 'label': '姓名', 'field': 'name', 'sortable': True},
    {'name': 'age', 'label': '年龄', 'field': 'age'},
    {'name': 'department', 'label': '部门', 'field': 'dept'}
]

# 行数据
rows = [
    {'id': 1, 'name': '张三', 'age': 28, 'dept': '研发部'},
    {'id': 2, 'name': '李四', 'age': 32, 'dept': '市场部'},
    {'id': 3, 'name': '王五', 'age': 25, 'dept': '人事部'}
]

# 创建表格
table = ui.table(columns=columns, rows=rows, row_key='id').classes('w-full')


table = ui.table(
    columns=columns,
    rows=rows,
    row_key='id',
    title='员工信息表',
    selection='multiple',
    pagination={'rowsPerPage': 5}
).classes('w-full h-96').props('''
    flat
    bordered
    dense
    grid
    hide-pagination
''')

import pandas as pd
from nicegui import ui

# 模拟异步数据获取
async def fetch_data(page: int, rows_per_page: int):
    # 实际项目这里可能是API请求
    df = pd.read_csv('flights.csv')
    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    return df.iloc[start:end].to_dict('records')

columns = [
    {'name': 'year', 'label': '年份', 'field': 'year'},
    {'name': 'month', 'label': '月份', 'field': 'month'},
    {'name': 'passengers', 'label': '乘客数', 'field': 'passengers'}
]

table = ui.table(
    columns=columns,
    rows=[],
    row_key='year',
    pagination={'rowsPerPage': 10}
).classes('w-full')

async def load_data():
    data = await fetch_data(1, 100)
    table.rows = data
    table.update()

ui.button('加载数据', on_click=load_data)


import pandas as pd
from nicegui import ui
from typing import Dict, Any

# 定义列
columns = [
    {'name': 'year', 'label': '年份', 'field': 'year', 'sortable': True},
    {'name': 'month', 'label': '月份', 'field': 'month', 'sortable': True},
    {'name': 'passengers', 'label': '乘客数', 'field': 'passengers', 'sortable': True}
]

async def fetch_paginated_data(
    page: int, 
    rows_per_page: int,
    sort_by: str = None,
    descending: bool = False
) -> Dict[str, Any]:
    df = pd.read_csv('flights.csv')
    
    # 排序处理
    if sort_by:
        df = df.sort_values(sort_by, ascending=not descending)
    
    total = len(df)
    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    return {
        'rows': df.iloc[start:end].to_dict('records'),
        'total': total
    }

# 创建表格
table = ui.table(
    columns=columns,
    rows=[],
    row_key='year',
    pagination={'rowsPerPage': 10}
).classes('w-full')

# 添加排序处理
def handle_sort(e):
    sort_column = e.args['sortBy']
    descending = e.args['descending']
    load_paginated_data(1, table.pagination['rowsPerPage'], sort_column, descending)

table.on('sort', handle_sort)

async def load_paginated_data(page, rows_per_page, sort_by=None, descending=False):
    result = await fetch_paginated_data(page, rows_per_page, sort_by, descending)
    table.rows = result['rows']
    table.pagination = {**table.pagination, 'total': result['total']}
    table.update()

# 初始加载数据
ui.button('加载数据', on_click=lambda: load_paginated_data(1, 10))

 
def show_selected():
    selected = table.selected
    if not selected:
        ui.notify('请选择行', type='warning')
        return
    names = ', '.join([row['name'] for row in selected])
    ui.notify(f'已选择: {names}')

table = ui.table(
    columns=[{'name': 'name', 'label': '姓名', 'field': 'name'}],
    rows=[{'name': '张三'}, {'name': '李四'}],
    row_key='name',
    selection='multiple'
)

ui.button('显示选择', on_click=show_selected)


import numpy as np 
 
# 生成10万行测试数据 
big_data = [{'id': i, 'value': np.random.randint(1000)}  for i in range(100000)]
 
# 创建表格 
table = ui.table( 
    columns=[
        {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
        {'name': 'value', 'label': 'Value', 'field': 'value'}
    ],
    rows=big_data,
    row_key='id',
    pagination={'rowsPerPage': 20}
).classes('h-96')
 
# 启用虚拟滚动（在2.15.0中需要通过其他方式实现）
table.props('virtual-scroll')   # 注意：在2.15.0中可能不支持 



from typing import AsyncGenerator

async def data_generator(chunk_size=1000) -> AsyncGenerator:
    """模拟大数据流式加载"""
    for i in range(0, 100000, chunk_size):
        chunk = [{'id': x, 'value': x*2} for x in range(i, i+chunk_size)]
        yield chunk
        await asyncio.sleep(0.1)  # 模拟网络延迟

table = ui.table(
    columns=[{'name': 'id', 'label': 'ID', 'field': 'id'}],
    rows=[],
    row_key='id'
)

async def load_streaming_data():
    async for chunk in data_generator():
        table.rows.extend(chunk)
        table.update()
    ui.notify('所有数据加载完成')
    
ui.run()