import warnings
from hypergol import Task
from data_models.raw_data import RawData
from data_models.comment import Comment
from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning

def get_clean_text(rawText):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)
        soup=BeautifulSoup(rawText, features='html.parser')
        for tag in soup.find_all(['a', 'pre', 'code']):
            tag.extract() 
        return soup.get_text(separator='\n')

class SelectComments(Task):

    def __init__(self, *args, **kwargs):
        super(SelectComments, self).__init__(*args, **kwargs)

    def run(self, rawData):
        if rawData.dead == 1 or rawData.deleted == 1:
            return
        if rawData.text == '':
            return
        if rawData.htype not in ['comment', 'story']:
            return
        self.output.append(Comment(
            text=get_clean_text(rawData.text),
            author=rawData.author,
            timestamp=rawData.timestamp,
            hid=rawData.hid,
            parent=rawData.parent 
        ))
