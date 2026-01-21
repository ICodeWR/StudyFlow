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

# Module/Script Name: employee.py
# Author: ICodeWR (微信公众号，头条号同名）
# Created: 2025-05
# Description: NiceGUI exexample Script.

import pandas as pd 
from nicegui import ui 
 
# 数据模型 
class Employee:
    def __init__(self, id, name, department, salary, join_date):
        self.id  = id 
        self.name  = name 
        self.department  = department 
        self.salary  = salary 
        self.join_date  = join_date 
 
# 模拟数据库 
class EmployeeDB:
    def __init__(self):
        self.data  = [
            Employee(1, '张三', '研发部', 15000, '2020-05-15'),
            Employee(2, '李四', '市场部', 12000, '2019-11-20'),
            Employee(3, '王五', '人事部', 10000, '2021-03-10'),
        ]
        self.next_id  = 4 
    
    def get_all(self):
        return [e.__dict__ for e in self.data] 
    
    def add(self, name, department, salary, join_date):
        self.data.append(Employee(self.next_id,  name, department, salary, join_date))
        self.next_id  += 1 
    
    def update(self, id, name, department, salary):
        for emp in self.data: 
            if emp.id  == id:
                emp.name  = name 
                emp.department  = department 
                emp.salary  = salary 
                break 
    
    def delete(self, id):
        self.data  = [emp for emp in self.data  if emp.id  != id]
 
# 主界面 
def create_employee_table():
    db = EmployeeDB()
    selected_employee = None 
    
    # 表格列定义 
    columns = [
        {'name': 'id', 'label': 'ID', 'field': 'id'},
        {'name': 'name', 'label': '姓名', 'field': 'name'},
        {'name': 'department', 'label': '部门', 'field': 'department'},
        {'name': 'salary', 'label': '薪资', 'field': 'salary'},
        {'name': 'join_date', 'label': '入职日期', 'field': 'join_date'},
    ]
    
    # 创建表格 
    table = ui.table( 
        columns=columns,
        rows=db.get_all(), 
        row_key='id',
        pagination={'rowsPerPage': 5},
    ).classes('w-full')
    
    # 刷新表格数据 
    def refresh_table():
        table.rows  = db.get_all() 
        table.update() 
    
    # 添加员工对话框 
    def add_dialog():
        with ui.dialog()  as dialog, ui.card(): 
            with ui.column(): 
                ui.label(' 添加新员工')
                name = ui.input(' 姓名')
                department = ui.select([' 研发部', '市场部', '人事部'], label='部门')
                salary = ui.number(' 薪资', value=10000)
                join_date = ui.input(' 入职日期', placeholder='YYYY-MM-DD')
                
                with ui.row(): 
                    ui.button(' 取消', on_click=dialog.close) 
                    ui.button(' 确认', on_click=lambda: (
                        db.add(name.value,  department.value,  float(salary.value),  join_date.value), 
                        refresh_table(),
                        dialog.close(), 
                        ui.notify(' 添加成功')
                    ))
        dialog.open() 
    
    # 编辑员工对话框 
    def edit_dialog(employee):
        with ui.dialog()  as dialog, ui.card(): 
            with ui.column(): 
                ui.label(f' 编辑员工: {employee["name"]}')
                name = ui.input(' 姓名', value=employee['name'])
                department = ui.select( 
                    ['研发部', '市场部', '人事部'], 
                    value=employee['department'], 
                    label='部门'
                )
                salary = ui.number(' 薪资', value=employee['salary'])
                
                with ui.row(): 
                    ui.button(' 取消', on_click=dialog.close) 
                    ui.button(' 保存', on_click=lambda: (
                        db.update(employee['id'],  name.value,  department.value,  float(salary.value)), 
                        refresh_table(),
                        dialog.close(), 
                        ui.notify(' 更新成功')
                    ))
        dialog.open() 
    
    # 删除确认对话框 
    def delete_confirm(employee_id):
        with ui.dialog()  as dialog, ui.card(): 
            with ui.column(): 
                ui.label(' 确认删除该员工吗？')
                with ui.row(): 
                    ui.button(' 取消', on_click=dialog.close) 
                    ui.button(' 确认删除', on_click=lambda: (
                        db.delete(employee_id), 
                        refresh_table(),
                        dialog.close(), 
                        ui.notify(' 已删除')
                    )).props('color=negative')
        dialog.open() 
    
    # 操作按钮 
    with ui.row().classes('w-full  items-center'):
        ui.button(' 添加员工', icon='add', on_click=add_dialog).props('color=positive')
        
        with ui.row().classes('ml-auto'): 
            # 编辑按钮（需要先选中行）
            edit_btn = ui.button(' 编辑', icon='edit', on_click=lambda: edit_dialog(selected_employee))
            edit_btn.disable() 
            
            # 删除按钮（需要先选中行）
            del_btn = ui.button(' 删除', icon='delete', on_click=lambda: delete_confirm(selected_employee['id']))
            del_btn.disable() 
    
    # 行选择处理 
    def on_row_select(e): 
        nonlocal selected_employee 
        selected_employee = e.args['row'] 
        edit_btn.enable() 
        del_btn.enable() 
    
    table.on('rowClick',  on_row_select)
    
    return table 
 
# 创建页面 
@ui.page('/') 
def main():
    ui.label(' 员工管理系统').classes('text-h4 my-4')
    create_employee_table()
 
ui.run(title=' 员工管理系统', port=8080)