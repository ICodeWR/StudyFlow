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

# Module/Script Name: registration_form.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day02 exexample Script.


# 创建表单组件
import panel as pn

pn.extension(notifications=True)  # 确保在启用通知功能

name = pn.widgets.TextInput(name='姓名', placeholder='请输入全名')
email = pn.widgets.TextInput(name='邮箱', placeholder='example@domain.com')
password = pn.widgets.PasswordInput(name='密码')
gender = pn.widgets.RadioBoxGroup(name='性别', options=['男', '女', '其他'], inline=True)
interests = pn.widgets.CheckBoxGroup(name='兴趣', options=['体育', '音乐', '阅读', '编程'])
birthday = pn.widgets.DatePicker(name='出生日期')
submit = pn.widgets.Button(name='注册', button_type='primary')

# 表单验证
def validate_form():
    errors = []
    if not name.value:
        errors.append("姓名不能为空")
    if '@' not in email.value:
        errors.append("邮箱格式不正确")
    if len(password.value) < 6:
        errors.append("密码至少需要6个字符")
    return errors

# 提交处理
def on_submit(event):
    errors = validate_form()
    if errors:
        # errors = [...]  # 你的错误收集逻辑
        if pn.state.notifications:
            pn.state.notifications.error("<br>".join(errors), duration=5000)
        else:
            # 备用错误处理
            pn.pane.Alert("错误: " + ", ".join(errors), alert_type="danger").servable()
    else:
        pn.state.notifications.success("注册成功！")
        # 这里可以添加实际提交逻辑

submit.on_click(on_submit)

# 组织表单布局
registration_form = pn.Column(
    pn.pane.Markdown("## 用户注册"),
    name,
    email,
    password,
    pn.Row(pn.Column("性别", gender), pn.Column("兴趣", interests)),
    birthday,
    submit,
    width=400
)

registration_form.servable()