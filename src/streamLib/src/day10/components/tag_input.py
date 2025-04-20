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

# Module/Script Name: tag_input.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
import streamlit.components.v1 as components

# 声明自定义组件
def tag_input(label, default=None, key=None):
    if default is None:
        default = []
    
    # 组件HTML/JS
    component_html = f"""
    <div id="tag-input-container">
        <style>
            .tag-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            .tag {{
                background-color: #f0f2f6;
                padding: 2px 8px;
                border-radius: 10px;
                display: flex;
                align-items: center;
            }}
            .tag-remove {{
                margin-left: 5px;
                cursor: pointer;
            }}
            #tag-input {{
                border: none;
                outline: none;
                flex-grow: 1;
                padding: 5px;
            }}
        </style>
        
        <label>{label}</label>
        <div class="tag-container" id="tags-{key}">
            <input type="text" id="tag-input-{key}" placeholder="输入标签后按回车...">
        </div>
        
        <script>
            const container = document.getElementById('tags-{key}');
            const input = document.getElementById('tag-input-{key}');
            const tags = {default};
            
            function updateTags() {{
                Streamlit.setComponentValue(tags);
            }}
            
            function createTag(label) {{
                const tagDiv = document.createElement('div');
                tagDiv.className = 'tag';
                
                const span = document.createElement('span');
                span.textContent = label;
                
                const removeBtn = document.createElement('span');
                removeBtn.className = 'tag-remove';
                removeBtn.innerHTML = '×';
                removeBtn.onclick = function() {{
                    const index = tags.indexOf(label);
                    if (index !== -1) {{
                        tags.splice(index, 1);
                        container.removeChild(tagDiv);
                        updateTags();
                    }}
                }};
                
                tagDiv.appendChild(span);
                tagDiv.appendChild(removeBtn);
                return tagDiv;
            }}
            
            // 初始化已有标签
            tags.forEach(tag => {{
                container.insertBefore(createTag(tag), input);
            }});
            
            input.addEventListener('keydown', function(e) {{
                if (e.key === 'Enter' && input.value.trim() !== '') {{
                    const tag = input.value.trim();
                    if (!tags.includes(tag)) {{
                        tags.push(tag);
                        container.insertBefore(createTag(tag), input);
                        updateTags();
                    }}
                    input.value = '';
                }}
            }});
        </script>
    </div>
    """
    
    # 渲染组件
    return components.html(component_html, height=100, key=key)

