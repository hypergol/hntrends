from datetime import datetime

from hypergol import BaseData


class RawData(BaseData):

    def __init__(self, title: str, url: str, text: str, dead: int, author: str, score: int, time: int, timestamp: datetime, htype: str, hid: int, parent: int, descendants: int, ranking: int, deleted: int):
        self.title = title
        self.url = url
        self.text = text
        self.dead = dead
        self.author = author
        self.score = score
        self.time = time
        self.timestamp = timestamp
        self.htype = htype
        self.hid = hid
        self.parent = parent
        self.descendants = descendants
        self.ranking = ranking
        self.deleted = deleted

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
