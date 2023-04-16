import requests
from utils import page_id


class Postman:
    def __init__(self, token):
        self.session = requests.Session()
        self.headers = {
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
        }
        self.session.headers.update(self.headers)

    # 给数据库新增一条数据
    def add_database_item(self, database_id, properties):
        res = self.post(f'https://api.notion.com/v1/pages', json={
            "parent": {"database_id": database_id},
            "properties": properties
        })
        return res.json()

    # 遍历中数据库的内容
    # item_handler是一个函数，接受一个item作为参数，用来操作每一条数据库记录
    def iterate_database(self, database_id, item_handler):
        res = self.post(f'https://api.notion.com/v1/databases/{database_id}/query', json={
            "page_size": 100
        })
        data = res.json()
        for item in data['results']:
            item_handler(item)
        cursor = data.get('next_cursor')
        while cursor is not None:
            res = self.post(f'https://api.notion.com/v1/databases/{database_id}/query', json={
                "start_cursor": cursor,
                "page_size": 100
            })
            data = res.json()
            for item in data['results']:
                item_handler(item)
            cursor = data.get('next_cursor')

    # 在页面中新建一个数据库
    def create_database(self, page_id, title, properties):
        res = self.post(f'https://api.notion.com/v1/databases', json={
            "parent": {"page_id": page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties
        })
        return res.json()

    # 向页面追加一段文字
    def append_text(self, page_id, text):
        return self.append_custom(page_id, {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": text
                                }
                            }
                        ]
                    }
                }
            ]
        })

    # 向页面追加自定义的内容，但需要调用函数的人自己保证json内容的正确性
    def append_custom(self, page_id, json):
        res = self.patch(f'https://api.notion.com/v1/blocks/{page_id}/children', json=json)
        return res.json()

    # 从页面读取块
    def read_blocks(self, page_id):
        res = self.get(f'https://api.notion.com/v1/blocks/{page_id}/children')
        return res.json()['results']

    # 创建一个界面
    def create_page(self, parent_id, title):
        res = self.post(f'https://api.notion.com/v1/pages', json={
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": title}}]
                }
            }
        })
        return res.json()

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.session.patch(*args, **kwargs)
