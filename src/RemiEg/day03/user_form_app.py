from remi import start, App, gui

class UserFormApp(App):
    def __init__(self, *args):
        super(UserFormApp, self).__init__(*args)

    def main(self):
        # 创建一个垂直布局容器作为根容器
        root_container = gui.VBox(width=400, style={'margin': 'auto', 'padding': '20px', 'border': '1px solid #ccc'})

        # 创建标题标签
        title = gui.Label("用户信息表单", style={'font-size': '24px', 'text-align': 'center', 'margin-bottom': '20px'})

        # 创建用户名输入项
        username_container = gui.HBox(width='100%', style={'margin-bottom': '10px'})
        username_label = gui.Label("用户名:", width=100, style={'font-size': '16px'})
        self.username_input = gui.TextInput(width=200, height=30)
        username_container.append(username_label)
        username_container.append(self.username_input)

        # 创建邮箱输入项
        email_container = gui.HBox(width='100%', style={'margin-bottom': '10px'})
        email_label = gui.Label("邮箱:", width=100, style={'font-size': '16px'})
        self.email_input = gui.TextInput(width=200, height=30)
        email_container.append(email_label)
        email_container.append(self.email_input)

        # 创建年龄输入项
        age_container = gui.HBox(width='100%', style={'margin-bottom': '20px'})
        age_label = gui.Label("年龄:", width=100, style={'font-size': '16px'})
        self.age_input = gui.TextInput(width=200, height=30)
        age_container.append(age_label)
        age_container.append(self.age_input)

        # 创建提交按钮
        submit_button = gui.Button("提交", width=100, height=30)
        submit_button.onclick.do(self.on_submit_clicked)

        # 创建结果显示标签
        self.result_label = gui.Label("", style={'font-size': '16px', 'text-align': 'center', 'margin-top': '20px'})

        # 将所有组件添加到根容器中
        root_container.append(title)
        root_container.append(username_container)
        root_container.append(email_container)
        root_container.append(age_container)
        root_container.append(submit_button)
        root_container.append(self.result_label)

        # 返回根容器
        return root_container

    def on_submit_clicked(self, widget):
        # 获取用户输入
        username = self.username_input.get_value()
        email = self.email_input.get_value()
        age = self.age_input.get_value()

        # 显示结果
        self.result_label.set_text(f"用户名: {username}, 邮箱: {email}, 年龄: {age}")

# 启动应用
if __name__ == "__main__":
    start(UserFormApp, address='0.0.0.0', port=8080)