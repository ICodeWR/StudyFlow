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

# Module/Script Name: crm.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day04 exexample Script.

import pandas as pd
import panel  as pn

# 基本初始化（必须在使用交互组件前调用）
pn.extension()

# 创建模拟数据
contacts = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六'],
    '职位': ['经理', '工程师', '设计师', '销售'],
    '公司': ['A公司', 'B公司', 'C公司', 'D公司'],
    '最后联系': pd.date_range('2023-01-01', periods=4),
    '状态': ['活跃', '休眠', '活跃', '新客户']
})

# 创建组件
search_bar = pn.widgets.TextInput(placeholder='搜索联系人...')
status_filter = pn.widgets.MultiSelect(name='状态', options=['活跃', '休眠', '新客户'], value=['活跃'])
contact_table = pn.widgets.Tabulator(contacts, page_size=5, selectable=True)

# 联系人详情面板
@pn.depends(contact_table.param.selection)
def contact_detail(selection):
    if not selection:
        return pn.pane.Markdown("请选择联系人")
    data = contacts.iloc[selection[0]]
    return pn.Column(
        pn.pane.Markdown(f"## {data['姓名']}"),
        pn.widgets.StaticText(name='职位', value=data['职位']),
        pn.widgets.StaticText(name='公司', value=data['公司']),
        pn.widgets.StaticText(name='状态', value=data['状态']),
        pn.widgets.TextAreaInput(name='备注', placeholder='添加备注...')
    )

# 创建布局
crm_layout = pn.template.FastGridTemplate(
    title='客户关系管理系统',
    theme='default',
    sidebar=[
        pn.pane.Markdown("## 筛选条件"),
        search_bar,
        status_filter
    ],
    main=[
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### 联系人列表"),
                contact_table,
                sizing_mode='stretch_both'
            ),
            pn.Column(
                pn.pane.Markdown("### 联系人详情"),
                contact_detail,
                sizing_mode='stretch_both'
            )
        )
    ],
    header_background='#2b8cbe',
    prevent_collision=True  # 防止组件ID冲突
)

crm_layout.servable()
