from datetime import datetime

from hypergol import BaseData


class Story(BaseData):

    def __init__(self, title: str, url: str, author: str, score: int, timestamp: datetime, hid: int, descendants: int):
        self.title = title
        self.url = url
        self.author = author
        self.score = score
        self.timestamp = timestamp
        self.hid = hid
        self.descendants = descendants

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
