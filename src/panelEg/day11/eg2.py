import param
import panel as pn

# 启用Panel扩展
pn.extension()

class CustomSlider(pn.reactive.ReactiveHTML):
    """自定义滑块组件 (Panel 1.6.2兼容版)"""
    
    # 定义参数
    value = param.Number(default=0.5, bounds=(0, 1))
    color = param.Color(default='#2b8cbe')
    disabled = param.Boolean(default=False)
    options = param.ListSelector(default=[])
    
    # HTML模板 (兼容1.6.2语法)
    _template = """
    <div style="padding: 20px;">
        <input id="slider"
            type="range" 
            min="0" max="1" step="0.01"
            value="${value}"
            style="accent-color: ${color}; width: 100%"
            disabled="${disabled}"
            oninput="${script('slider_change')}"
        > Test </input>
        <p>当前值: <span id="span" style="font-weight: bold; color: ${color}">${value.toFixed(2)}</span></p>
    </div>
    """
    
    # JavaScript回调 (兼容1.6.2语法)
    _scripts = {
        'slider_change': """
            data.value = parseFloat(event.target.value);
        """,
        'render': """
            // 初始化时更新显示
            console.log('Slider initialized with value:', this.value);
        """,
        'options': """
            this.update_options();
        """
    }
    
    def __init__(self, **params):
        super().__init__(**params)
        # 添加选项变化回调
        self.param.watch(self._update_options, 'options')

    def _update_options(self, event):
        # 手动触发前端更新
        if self.options == ["Low"]:
            self.value = 0
        elif self.options == ["Medium"]:
            self.value = 0.5
        elif self.options == ["High"]:
            self.value = 1
        self.param.trigger('value')

# 创建示例数据
slider = CustomSlider(
    name="自定义滑块",
    color="#ff6b6b",
    options=['Low', 'Medium', 'High']
)

# 创建控制面板
controls = pn.Param(
    slider,
    parameters=['value', 'color', 'disabled', 'options'],
    sizing_mode='stretch_width'
)

# 创建布局
app = pn.Column(
    pn.pane.Markdown("## 自定义滑块演示 (Panel 1.6.2)"),
    slider,
    pn.Accordion(("参数控制", controls)),
    sizing_mode='stretch_width'
)


# 启动服务器
app.servable()