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
# Description: streamlit day01 exexample Script.

import streamlit as st

# 设置页面标题
st.title("Hello Streamlit!")

# 显示文本
st.write("这是我的第一个 Streamlit 应用！")

# 显示数据框
import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
st.write("这是一个数据框：")
st.write(df)

# st.write("调试信息：", df.shape)
