import param
import panel as pn

class CustomCounter(pn.reactive.ReactiveHTML):
    # 定义参数
    value = param.Integer(default=0, bounds=(0, None))
    
    # HTML模板
    _template = """
    <div style="border: 2px solid #2b8cbe; padding: 20px; border-radius: 5px; text-align: center;">
        <p>当前计数: ${value}</p>
        <button id="inc" onclick="${script('increment')}">增加</button>
        <button id="dec" onclick="${script('decrement')}">减少</button>
    </div>
    """
    
    # JavaScript回调
    _scripts = {
        'increment': 'data.value += 1',
        'decrement': 'data.value -= 1'
    }

# 使用组件
counter = CustomCounter(name='我的计数器')
counter.servable(title='计数器')