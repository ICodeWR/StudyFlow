from nicegui import ui

def handle_action(action: str):
    ui.notify(f"执行操作: {action}")

# 主工具栏
with ui.button_group().classes("w-full justify-center p-4 gap-2"):
    # 文件操作组
    with ui.button_group():
        ui.button("新建", icon="create", on_click=lambda: handle_action("new"))
        ui.button("打开", icon="folder_open")
    
    # 编辑操作组
    with ui.button_group():
        ui.button("剪切", icon="content_cut")
        ui.button("复制", icon="content_copy")
        ui.button("粘贴", icon="content_paste")
    
    # 功能按钮
    ui.button("保存", icon="save", color="green")
    ui.button("打印", icon="print")
    
    # 危险操作下拉
    with ui.button(icon="warning", color="red"):
        with ui.menu():
            ui.menu_item("清空回收站", on_click=lambda: handle_action("empty_trash"))
            ui.menu_item("重置系统", on_click=lambda: handle_action("reset"))

# 状态栏
with ui.row().classes("w-full justify-between p-2 bg-gray-100"):
    ui.button("帮助", icon="help")
    ui.button("用户", icon="account_circle")
    ui.button("设置", icon="settings")

ui.run()