import csv
import gzip
import glob
from datetime import datetime
from hypergol import Source
from data_models.raw_data import RawData


class LoadData(Source):

    def __init__(self, filePattern, *args, **kwargs):
        super(LoadData, self).__init__(*args, **kwargs)
        # for example: '/data/hn-full-20201129/hn-full-20201129-*'
        self.filePattern = filePattern

    def source_iterator(self):
        hnfiles = glob.glob(self.filePattern)
        for hnfile in hnfiles:
            with gzip.open(hnfile, 'rt') as csvfile:
                for row in csv.DictReader(csvfile):
                    yield row

    def run(self, data):
        rawData = RawData(
            title=data['title'], 
            url=data['url'], 
            text=data['text'], 
            dead=1 if data['dead']=='true' else 0,
            author=data['by'],
            score=int(data['score']),
            time=int(data['time']),
            timestamp=datetime.fromisoformat(data['timestamp'][:19].replace(' ','T')),
            htype=data['type'],
            hid=int(data['id']),
            parent=int(data['parent']),
            descendants=int(data['descendants']),
            ranking=int(data['ranking']),
            deleted=1 if data['deleted']=='true' else 0
        )
        return exampleOutputObject
