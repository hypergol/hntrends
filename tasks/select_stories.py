from hypergol import Task
from data_models.raw_data import RawData
from data_models.story import Story


class SelectStories(Task):

    def __init__(self, *args, **kwargs):
        super(SelectStories, self).__init__(*args, **kwargs)

    def run(self, rawData):
        if rawData.dead == 1 or rawData.deleted == 1:
            return
        if rawData.htype == 'story':
            if rawData.title == '' and rawData.url == '':
                return
            self.output.append(Story(
                title=rawData.title,
                url=rawData.url,
                author=rawData.author,
                score = rawData.score,
                timestamp = rawData.timestamp,
                hid=rawData.hid,
                descendants =rawData.descendants
            ))