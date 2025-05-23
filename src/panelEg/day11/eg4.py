
import param
import panel as pn

class CollapsiblePanel(pn.reactive.ReactiveHTML):
    title = param.String(default="面板标题")
    collapsed = param.Boolean(default=True)
    contents = param.Parameter(default=None)
    
    # 子组件插槽
    _child_config = {
        'contents': 'model'
    }
    
    _template = """
    <div style="margin-bottom: 10px;">
        <div id="div11"
            onclick="${script('toggle')}" 
            style="
                background: #f0f0f0;
                padding: 10px;
                cursor: pointer;
                border-radius: 4px;
                display: flex;
                justify-content: space-between;
            "
        >
            <span>{{title}}</span>
            <span id="icon">▼</span>
        </div>

        <div class="collapsible-content" id="content">
            <slot></slot>
        </div>
       
        <div id="contents" style="
            padding: 10px;
            border: 1px solid #f0f0f0;
            border-top: none;
            display: ${collapsed} ? 'none' : 'block'};
        ">
            ${contents}
        </div>
    </div>
    """
    
    _scripts = {
        'toggle': """
        if (data.collapsed)  {
                content.style.maxHeight  = content.scrollHeight  + "20px";
                icon.style.transform  = "rotate(180deg)";
            } else {
                content.style.maxHeight  = "0";
                icon.style.transform  = "rotate(0deg)";
            }
            data.collapsed  = !data.collapsed; 
        """
    }
    _stylesheets = ["""
    .collapsible-content {
        padding: 0 10px;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.2s ease-out;
    }
    #icon {
        transition: transform 0.2s;
    }
    """]

# 使用示例
panel = CollapsiblePanel(
    title="高级设置",
    contents=pn.Column(
        pn.widgets.Checkbox(name="选项1"),
        pn.widgets.Select(name="模式", options=["A", "B"])
    )
).servable(title="可折叠面板")