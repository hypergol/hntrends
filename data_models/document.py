from typing import List
from datetime import datetime

from hypergol import BaseData


class Document(BaseData):

    def __init__(self, hid: int, timestamp: datetime, tokens: List[str], labels: List[str]):
        self.hid = hid
        self.timestamp = timestamp
        self.tokens = tokens
        self.labels = labels

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
