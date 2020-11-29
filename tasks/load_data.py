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
        self.intColumnsWithEmptyString = set()
        self.intColumnsWithMinusOne = set()

    def source_iterator(self):
        hnfiles = glob.glob(self.filePattern)
        for hnfile in hnfiles:
            with gzip.open(hnfile, 'rt') as csvfile:
                for row in csv.DictReader(csvfile):
                    yield row
        self.logger.log(f'Found special columns:\n  intColumnsWithEmptyString:{self.intColumnsWithEmptyString}\n  intColumnsWithMinusOne:{self.intColumnsWithMinusOne}')

    def run(self, data):
        def safe_int(columnName, value):
            if value == '':
                self.intColumnsWithEmptyString.add(columnName)
                return -1
            if value =='-1':
                self.intColumnsWithMinusOne.add(columnName)
            return int(value)

        if data['timestamp'] == '':
            timestamp = datetime.min
        else
            timestamp = datetime.fromisoformat(data['timestamp'][:19].replace(' ','T'))

        rawData = RawData(
            title=data['title'], 
            url=data['url'], 
            text=data['text'], 
            dead=1 if data['dead']=='true' else 0,
            author=data['by'],
            score=safe_int('score', data['score']),
            time=safe_int('time', data['time']),
            timestamp=timestamp,
            htype=data['type'],
            hid=int(data['id']),
            parent=safe_int('parent', data['parent']),
            descendants=safe_int('descendants', data['descendants']),
            ranking=safe_int('ranking', data['ranking']),
            deleted=1 if data['deleted']=='true' else 0
        )
        return rawData
