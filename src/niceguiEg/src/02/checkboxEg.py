from nicegui import ui

agree = ui.checkbox('我同意用户协议')
ui.label().bind_text_from(agree, 'value', 
                         backward=lambda v: f'协议状态: {"已同意" if v else "未同意"}')

ui.run()