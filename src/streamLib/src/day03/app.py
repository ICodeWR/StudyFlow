#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Module/Script Name: app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day03 exexample Script.

import streamlit as st

# 标题和简介
st.title("用户注册表单")
st.write("请填写以下信息完成注册。")

# 姓名输入
name = st.text_input("请输入您的姓名")

# 年龄选择
age = st.slider("选择您的年龄", 0, 100, 25)

# 性别选择
gender = st.selectbox("选择您的性别", ["男", "女", "其他"])

# 兴趣爱好选择
hobbies = st.multiselect("选择您的兴趣爱好", ["阅读", "运动", "音乐", "旅行"])

# 上传头像
uploaded_file = st.file_uploader("上传您的头像", type=["jpg", "png"])

# 同意条款
agree = st.checkbox("我同意条款")

# 提交按钮
if st.button("提交"):
    if not name:
        st.error("请输入您的姓名！")
    elif not agree:
        st.error("请同意条款！")
    else:
        st.success("注册成功！")
        st.write("### 用户信息")
        st.write(f"**姓名:** {name}")
        st.write(f"**年龄:** {age}")
        st.write(f"**性别:** {gender}")
        st.write(f"**兴趣爱好:** {', '.join(hobbies)}")
        if uploaded_file is not None:
            st.write("**头像:**")
            st.image(uploaded_file, width=100)
