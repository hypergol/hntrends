from typing import List
from datetime import datetime

from hypergol import BaseData


class Element(BaseData):

    def __init__(self, date: str, timestamp: datetime, hid: str, parent: str, author: str, entities: List[str]):
        self.date = date
        self.timestamp = timestamp
        self.hid = hid
        self.parent = parent
        self.author = author
        self.entities = entities

    def get_id(self):
        return (self.date, )

    def to_data(self):
        data = self.__dict__.copy()
        data['timestamp'] = data['timestamp'].isoformat()
        return data

    @classmethod
    def from_data(cls, data):
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
