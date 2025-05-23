import param
import panel as pn

# 启用Panel扩展
pn.extension()

class DashboardCard(pn.reactive.ReactiveHTML):
    """仪表盘指标卡片组件 (Panel 1.6.2兼容版)"""
    
    title = param.String(default="指标卡")
    value = param.Number(default=0)
    trend = param.Number(default=0)  # 正数表示上升，负数表示下降
    
    _template = """
    <div class="dashboard-card" style="
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h3 id="h3">"${title}"</h3>
        <div id="idv22" style="font-size: 24px; font-weight: bold; margin: 10px 0;">
            {{value}}
        </div>
        
      
        <div id="div33" style="color: {{'green' if trend >= 0 else 'red'}};">
            {{'↑' if trend >= 0 else '↓'}} {{"%.1f"|format((trend))}} %
        </div>


    </div>
    """
    
    # 使用Jinja2模板引擎
    _child_config = {
        'title': 'literal',
        'value': 'literal',
        'trend': 'literal'
    }
    
    # CSS样式
    _stylesheets = ["""
    .dashboard-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: box-shadow 0.3s;
    }
    """]

# 创建示例卡片
sales_card = DashboardCard(
    title="销售额", 
    value=12560, 
    trend=12.5
)

profit_card = DashboardCard(
    title="利润率", 
    value=32.8, 
    trend=-2.3
)

# 创建仪表盘布局
dashboard = pn.Row(
    sales_card,
    profit_card,
    sizing_mode='stretch_width'
)

# 启动服务器
dashboard.servable(title="仪表盘卡片示例")