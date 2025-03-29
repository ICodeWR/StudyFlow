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

# Module/Script Name: 09app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day09 exexample Script.

import streamlit as st
import numpy as np
import pandas as pd
import torch
from torchvision import models, transforms
from PIL import Image

# 初始化会话状态
if "model" not in st.session_state:
    st.session_state.model = None
if "class_labels" not in st.session_state:
    st.session_state.class_labels = None

# 模型加载（带缓存）
@st.cache_resource
def load_model():
    # 加载预训练模型
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
    model.eval()
    
    # 加载标签文件
    with open("imagenet_classes.txt") as f:
        class_labels = [line.strip() for line in f]
    
    return model, class_labels

# 图片预处理
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    return transform(image).unsqueeze(0)

# 结果可视化
def show_results(probs, labels):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption="输入图片")
        
    with col2:
        st.subheader("预测结果")
        
        # 显示 Top-5 结果
        top5_probs, top5_indices = torch.topk(probs, 5)
        for i, (prob, idx) in enumerate(zip(top5_probs, top5_indices)):
            st.progress(float(prob), 
                       text=f"{i+1}. {labels[idx]} ({prob*100:.2f}%)")
        
        # 置信度分布图
        with st.expander("查看完整置信度分布"):
            probs_np = probs.detach().numpy()
            chart_data = pd.DataFrame({
                "Class": labels,
                "Confidence": probs_np
            }).sort_values("Confidence", ascending=False).head(20)
            st.bar_chart(chart_data.set_index("Class"))

# 主界面
st.title("🖼️ 智能图像分类系统")
st.markdown("使用 ResNet-50 实现 ImageNet 1000 类物体识别")

# 侧边栏控制面板
with st.sidebar:
    st.header("模型控制")
    if st.button("初始化/重新加载模型"):
        with st.spinner("加载模型中..."):
            st.session_state.model, st.session_state.class_labels = load_model()
            st.toast("模型加载成功!", icon="✅")
    
    st.divider()
    st.write("模型信息：")
    if st.session_state.model:
        st.code(f"ResNet-50\n参数量：{sum(p.numel() for p in st.session_state.model.parameters()):,}")

# 主内容区
with st.container():
    uploaded_file = st.file_uploader(
        "上传图片文件", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=False
    )
    
    if uploaded_file and st.session_state.model:
        # 读取并预处理图片
        image = Image.open(uploaded_file).convert("RGB")
        input_tensor = preprocess_image(image)
        
        # 执行预测
        with st.spinner("模型推理中..."):
            with torch.no_grad():
                output = st.session_state.model(input_tensor)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        # 显示结果
        show_results(probabilities, st.session_state.class_labels)
        
    elif not st.session_state.model:
        st.warning("请先在侧边栏初始化模型")
