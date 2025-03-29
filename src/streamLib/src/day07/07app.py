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

# Module/Script Name: 07app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day07 exexample Script.

import streamlit as st

# 初始化会话状态
def initialize_state():
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "products" not in st.session_state:
        st.session_state.products = {
            "iPhone 15": 7999,
            "MacBook Pro": 14999,
            "AirPods Pro": 1999
        }

initialize_state()

# 页面标题
st.title("🛒 Streamlit 购物车系统")

# 主界面布局
col1, col2 = st.columns([3, 1])

# 左侧商品展示
with col1:
    st.header("商品列表")
    for product, price in st.session_state.products.items():
        subcol1, subcol2 = st.columns([2, 1])
        with subcol1:
            st.write(f"### {product}")
            st.write(f"价格: ¥{price}")
        with subcol2:
            if st.button(f"加入购物车", key=f"add_{product}"):
                if product in st.session_state.cart:
                    st.session_state.cart[product] += 1
                else:
                    st.session_state.cart[product] = 1
                st.rerun()

# 右侧购物车
with col2:
    st.header("购物车")
    
    if not st.session_state.cart:
        st.write("购物车为空")
    else:
        total = 0
        for product, quantity in st.session_state.cart.items():
            with st.expander(f"{product} ({quantity})"):
                st.write(f"单价: ¥{st.session_state.products[product]}")
                st.write(f"小计: ¥{st.session_state.products[product] * quantity}")
                if st.button(f"❌ 移除", key=f"del_{product}"):
                    del st.session_state.cart[product]
                    st.rerun()
            total += st.session_state.products[product] * quantity
        
        st.divider()
        st.subheader(f"总价: ¥{total}")
        
        if st.button("清空购物车"):
            st.session_state.cart = {}
            st.rerun()

# 侧边栏操作面板
with st.sidebar:
    st.header("操作面板")
    st.write(f"商品总数: {sum(st.session_state.cart.values())}")
    
    if st.button("🔄 刷新页面"):
        st.rerun()
    
    with st.expander("调试信息"):
        st.write("会话状态内容:")
        st.write(st.session_state)
        