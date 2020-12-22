import numpy as np
from gensim.models.doc2vec import Doc2Vec
from hypergol import Task
from data_models.document import Document
from data_models.element import Element

class EpochSaver:
    pass

class CreateElements(Task):

    def __init__(self, modelPath, *args, **kwargs):
        super(CreateElements, self).__init__(*args, **kwargs)
        self.modelPath = modelPath

    def init(self):
        self.log('Model Load - START')
        self.model = Doc2Vec.load(self.modelPath)
        self.log('Model Load - END')

    def run(self, document):
        hid = f'hn{document.hid}'
        parent = next((l for l in document.labels if l!=hid and l.startswith('hn')), '')
        author = next((l for l in document.labels if l.startswith('@')), '')
        nonEntities = {hid, parent, author}
        offset = self.model.docvecs.doctags[hid].offset
        vector = self.model.docvecs.vectors_docs[offset, :]
        self.output.append(Element(
            date=str(document.timestamp)[:10],
            timestamp=document.timestamp,
            hid=hid,
            parent=parent,
            author=author,
            entities=[l for l in document.labels if l not in nonEntities],
            vector=vector / np.sqrt(np.sum(np.power(vector, 2)))
        ))