from hypergol import Task
from data_models.document import Document
from data_models.element import Element


class CreateElements(Task):

    def __init__(self, *args, **kwargs):
        super(CreateElements, self).__init__(*args, **kwargs)

    def run(self, document):
        hid=f'hn{document.hid}'
        parent=next((l for l in document.labels if l!=hid and l.startswith('hn')), '')
        author=next((l for l in document.labels if l.startswith('@')), '')
        nonEntities = {hid, parent, author}
        self.output.append(Element(
            date=str(document.timestamp)[:10],
            timestamp=document.timestamp
            hid=hid,
            parent=parent,
            author=author,
            entities=[l for l in document.labels if l not in nonEntities]
        )
