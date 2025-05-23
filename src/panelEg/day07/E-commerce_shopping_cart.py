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

# Module/Script Name: E-commerce_shopping_cart.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-04
# Description: panel day07 exexample Script.

import panel  as pn
import param

class ShoppingCart(param.Parameterized):
    items = param.Dict(default={})
    total = param.Number(0.0)
    
    @param.depends('items', watch=True)  # 添加 watch=True 自动触发更新
    def update_total(self):
        self.total = sum(item['price']*item['qty'] for item in self.items.values())
    
    def add_item(self, product_id, name, price):
        if product_id in self.items:
            self.items[product_id]['qty'] += 1
        else:
            self.items[product_id] = {'name': name, 'price': price, 'qty': 1}
        self.param.trigger('items')
    
    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]
            self.param.trigger('items')

class ProductCatalog:
    products = {
        'p1': {'name': '无线耳机', 'price': 299},
        'p2': {'name': '智能手表', 'price': 599},
        'p3': {'name': '电子书阅读器', 'price': 899}
    }
    
    def product_card(self, cart):
        cards = []
        for pid, info in self.products.items():
            btn = pn.widgets.Button(
                name=f"加入购物车 {info['name']}", 
                button_type='primary'
            )
            btn.on_click(lambda e, p=pid: cart.add_item(p, **self.products[p]))
            cards.append(pn.Row(info['name'], f"¥{info['price']}", btn))
        return pn.Column(*cards)

cart = ShoppingCart()
catalog = ProductCatalog()

@pn.depends(cart.param.items)
def cart_view(items):
    rows = []
    for pid, item in items.items():
        row = pn.Row(
            item['name'],
            pn.widgets.IntInput(value=item['qty'], width=60),
            f"¥{item['price']}",
            pn.widgets.StaticText(value=f"¥{item['price']*item['qty']}"),
            pn.widgets.Button(
                name='❌', 
                button_type='light',
                width=30,
                on_click=lambda e, p=pid: cart.remove_item(p)
            )
        )
        rows.append(row)
    return pn.Column(
        pn.pane.Markdown("## 购物车"),
        *rows,
        pn.pane.Markdown(f"### 总计: ¥{cart.total}")
    )

dashboard = pn.Column(
    pn.Row(
        catalog.product_card(cart), 
        cart_view
    ),
    sizing_mode='stretch_width'
)
dashboard.servable()