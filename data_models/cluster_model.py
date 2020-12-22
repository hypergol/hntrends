from hypergol import BaseData


class ClusterModel(BaseData):

    def __init__(self, date: str, model: object):
        self.date = date
        self.model = model

    def get_id(self):
        return (self.date, )

    def to_data(self):
        data = self.__dict__.copy()
        data['model'] = BaseData.to_string(data['model'])
        return data

    @classmethod
    def from_data(cls, data):
        data['model'] = BaseData.from_string(data['model'])
        return cls(**data)
