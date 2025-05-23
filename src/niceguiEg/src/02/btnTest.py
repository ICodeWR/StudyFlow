from nicegui import ui

def say_hello():
    ui.notify("你好，NiceGui！")

ui.button("点击问候", on_click=say_hello)

ui.button("危险操作", color="red", icon="warning")

ui.button(icon="favorite", color="red")
ui.button("收藏", icon="favorite")

# 图标在右侧
ui.button("下一页", icon="arrow_forward").props("icon-right")

# 自定义图标颜色
ui.button("设置", icon="settings").props("icon-color=green")

disabled_btn = ui.button("不可点击", on_click=lambda: None)
disabled_btn.disable()
# 或
# ui.button("注册", enabled=False)


async def long_operation():
    with loading_btn:
        await some_async_operation()

loading_btn = ui.button("处理中...")
loading_btn.on_click(long_operation)

with ui.button_group():
    ui.button("保存", icon="save")
    ui.button("取消", icon="cancel")


with ui.button_group().classes("flex-col"):
    ui.button("上", icon="arrow_upward")
    ui.button("下", icon="arrow_downward")


with ui.button(icon="add", color="primary").props("fab"):
    with ui.menu():
        ui.menu_item("新建文件")
        ui.menu_item("新建文件夹")


debounce_timer = None 
 
def debounced_action():
    ui.notify(" 操作执行")
 
def on_button_click():
    global debounce_timer 
    if debounce_timer:
        debounce_timer.cancel() 
    debounce_timer = ui.timer(1.0,  debounced_action, once=True)
 
ui.button(" 提交").on("click", on_button_click) 


def show_confirm():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("确认删除？")
            with ui.row():
                ui.button("确认", on_click=lambda: (delete_item(), dialog.close()))
                ui.button("取消", on_click=dialog.close)
    dialog.open()

ui.button("删除", color="red", on_click=show_confirm)


# 右对齐按钮组
with ui.row().classes("w-full justify-end"):
    ui.button("取消")
    ui.button("保存", color="primary")

# 固定底部按钮
with ui.column().classes("h-screen relative"):
    content = ui.label("页面内容").classes("flex-grow")
    with ui.row().classes("absolute bottom-4 right-4"):
        ui.button("帮助")
        ui.button("下一步", color="primary")

ui.button("提交").props("aria-label=Submit form")

ui.button("测试").style("border: 1px solid red")  # 添加调试边框



ui.add_head_html('<link href="path/to/icons.css" rel="stylesheet">')


ui.run()