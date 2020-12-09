import sys
import csv
import gzip
import glob
from datetime import datetime
from hypergol import Job
from hypergol import Task
from data_models.raw_data import RawData


class LoadData(Task):

    def __init__(self, filePattern, *args, **kwargs):
        super(LoadData, self).__init__(*args, **kwargs)
        # for example: '/data/hn-full-20201129/hn-full-20201129-*'
        self.filePattern = filePattern

    def get_jobs(self):
        hnfiles = glob.glob(self.filePattern)
        return [Job(
            id_=jobId, 
            total=len(hnfiles)
            parameters={'hnfile': hnfile}
        ) for jobId, hnfile in enumerate(hnfiles)]

    def source_iterator(self, parameters):
        hnfile = parameters['hnfile']
        with gzip.open(hnfile, 'rt') as csvfile:
            for row in csv.DictReader(csvfile):
                yield (row, )

    def run(self, data):
        def safe_int(columnName, value):
            if value == '':
                return -sys.maxsize
            return int(value)

        if data['timestamp'] == '':
            timestamp = datetime.min
        else:
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
        self.output.append(rawData)
