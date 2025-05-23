from nicegui import ui

hobbies = {
    'reading': '阅读',
    'sports': '运动',
    'music': '音乐'
}

selected = []
for key, label in hobbies.items():
    cb = ui.checkbox(label)
    selected.append((key, cb))

ui.button('提交', on_click=lambda: ui.notify(
    f'选择了: {[label for key, (k, cb) in zip(hobbies.keys(), selected) if cb.value]}'
))

gender = ui.radio(
    ['男', '女'],
    value='男',
).props('inline')

payment_method = ui.radio({'alipay': '支付宝', 'wechat': '微信支付','card': '银行卡'}, value='alipay').props('inline')

with ui.teleport(f'#c{payment_method.id} > div:nth-child(1) .q-radio__label'):
    ui.icon('alipay', size='md')

with ui.teleport(f'#c{payment_method.id} > div:nth-child(2) .q-radio__label'):
    ui.icon('wechat', size='md')
         
with ui.teleport(f'#c{payment_method.id} > div:nth-child(3) .q-radio__label'):
    ui.icon('credit_card', size='md')

dark_mode = ui.toggle(
    [False, True],
    value=False,
    on_change=lambda e: ui.dark_mode().toggle()
)

ui.label().bind_text_from(dark_mode, 'value', 
                         backward=lambda v: f'暗黑模式: {"开启" if v else "关闭"}')


toggle = ui.toggle(
    ['OFF', 'ON'],
    value='OFF',
).classes('w-32 h-10')


fruit = ui.select(
    ['苹果', '香蕉', '橙子'],
    label='选择水果'
)


countries = ['中国', '日本', '韩国', '美国', '英国', '法国', '德国']

ui.select(
    options=countries,
    multiple=True,
    value = ['中国'],
    label='选择国家'
)


# 三级联动数据
region_data = {
    '华东': ['上海', '江苏', '浙江'],
    '华北': ['北京', '天津', '河北']
}

city_data = {
    '上海': ['黄浦区', '徐汇区', '浦东新区'],
    '北京': ['朝阳区', '海淀区', '西城区']
}

# 创建选择器
province = ui.select(
    list(region_data),
    label='省份'
)

city = ui.select(
    [],
    label='城市'
).bind_visibility_from(province, 'value')

district = ui.select(
    [],
    label='区县'
).bind_visibility_from(city, 'value')

# 联动逻辑
def update_cities():
    city.set_options(region_data.get(province.value, []))
    city.value = None
    district.options = []

province.on('update:model-value', lambda _: update_cities())

def update_districts():
    district.set_options(city_data[city.value])

city.on('update:model-value', lambda _: update_districts())


# 实时过滤示例
search = ui.input('搜索')
select = ui.select(['Python', 'Java', 'JavaScript'])

def filter_options():
    keyword = search.value.lower()
    select.set_options([lang for lang in ['Python', 'Java', 'JavaScript'] 
                     if keyword in lang.lower()])

search.on('update:model-value', filter_options)


# 虚拟滚动选择器
large_data = [f'选项 {i}' for i in range(1000)]
ui.select(
    options=large_data,
    label='大数据选择',
).classes('w-full').props('use-chips virtual-scroll')


ui.run()
