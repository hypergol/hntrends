import sys
import gzip
import glob
import pandas as pd
from datetime import datetime
from hypergol import Source
from data_models.raw_data import RawData


class LoadData(Source):

    def __init__(self, filePattern, logAtEachN, *args, **kwargs):
        super(LoadData, self).__init__(*args, **kwargs)
        # for example: '/data/hn-full-20201129/hn-full-20201129-*'
        self.filePattern = filePattern
        self.logAtEachN = logAtEachN

    def source_iterator(self):
        hnfiles = glob.glob(self.filePattern)
        for hnfile in hnfiles:
            hnDataframe=pd.read_csv(gzip.open(hnfile,'rt'), dtype=object, na_filter=False)
            for k, row in enumerate(hnDataframe.itertuples(index=False)):
                if k % self.logAtEachN == 0:
                    self.logger.log(f'Processed: {hnfile}: {k}/{len(hnDataframe)}')
                yield row

    def run(self, data):
        def safe_int(value):
            if value == '':
                return -sys.maxsize
            return int(value)

        if data.timestamp == '':
            timestamp = datetime.min
        else:
            timestamp = datetime.fromisoformat(data.timestamp[:19].replace(' ','T'))

        rawData = RawData(
            title=data.title, 
            url=data.url, 
            text=data.text, 
            dead=1 if data.dead=='true' else 0,
            author=data.by,
            score=safe_int(data.score),
            time=safe_int(data.time),
            timestamp=timestamp,
            htype=data.type,
            hid=int(data.id),
            parent=safe_int(data.parent),
            descendants=safe_int(data.descendants),
            ranking=safe_int(data.ranking),
            deleted=1 if data.deleted=='true' else 0
        )
        return rawData
