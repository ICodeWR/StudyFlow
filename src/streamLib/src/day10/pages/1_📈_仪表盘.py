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

# Module/Script Name: 1_📈_仪表盘.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import query_db

st.title("📈 数据仪表盘")

# 获取数据
@st.cache_data(ttl=300)
def get_dashboard_data():
    sales_data = query_db("SELECT * FROM sales WHERE date >= date('now', '-30 days')")
    user_data = query_db("SELECT * FROM users")
    return sales_data, user_data

sales_df, users_df = get_dashboard_data()

# 指标卡片
col1, col2, col3 = st.columns(3)
col1.metric("总销售额", f"¥{sales_df['amount'].sum():,.2f}", "7.2%")
col2.metric("活跃用户", len(users_df[users_df['status'] == 'active']), "-3.1%")
col3.metric("平均订单", f"¥{sales_df['amount'].mean():,.2f}", "1.8%")

# 图表展示
tab1, tab2, tab3 = st.tabs(["销售趋势", "用户分布", "产品分析"])

with tab1:
    fig = px.line(sales_df.groupby('date').sum().reset_index(), 
                 x='date', y='amount',
                 title="30天销售趋势")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("用户地域分布")
        region_count = users_df['region'].value_counts().reset_index()
        st.bar_chart(region_count, x='region', y='count')
    with col2:
        st.subheader("用户状态")
        status_count = users_df['status'].value_counts().reset_index()
        fig = px.pie(status_count, 
                    values='count', 
                    names='status',
                    title='用户状态分布')
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    product_sales = sales_df.groupby('product_id').agg({
        'amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    fig = px.scatter(product_sales, x='quantity', y='amount', size='amount',
                    hover_name='product_id', title="产品销量与销售额关系")
    st.plotly_chart(fig, use_container_width=True)

    