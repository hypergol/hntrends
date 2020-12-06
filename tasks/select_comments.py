from hypergol import Task
from data_models.raw_data import RawData
from data_models.comment import Comment


class SelectComments(Task):

    def __init__(self, *args, **kwargs):
        super(SelectComments, self).__init__(*args, **kwargs)

    def run(self, rawData):
        if rawData.dead == 1 or rawData.deleted == 1:
            return
        if rawData.text == '':
            return
        if rawData.htype in ['comment', 'story']:
            self.output.append(Comment(
                text=rawData.text,
                author=rawData.author,
                timestamp=rawData.timestamp,
                hid=rawData.hid,
                parent=rawData.parent 
            ))
