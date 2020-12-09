from datetime import datetime

from hypergol import BaseData


class Comment(BaseData):

    def __init__(self, text: str, author: str, timestamp: datetime, hid: int, parent: int):
        self.text = text
        self.author = author
        self.timestamp = timestamp
        self.hid = hid
        self.parent = parent

    def get_id(self):
        return (self.hid, )

    def to_data(self):
        data = self.__dict__.copy()
        data['timestamp'] = data['timestamp'].isoformat()
        return data

    @classmethod
    def from_data(cls, data):
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
