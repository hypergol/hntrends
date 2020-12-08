import sys
import spacy
from hypergol import Task
from data_models.document import Document

# replace -> swap the sf with the type
# keep -> extract NER as a label
# ignore -> do nothing
NER_CHANGES = {
    'CARDINAL': 'replace',
    'PERSON': 'keep',
    'TIME': 'replace',
    'WORK_OF_ART': 'keep',
    'ORG': 'keep',
    'DATE': 'replace',
    'GPE': 'keep',
    'PRODUCT': 'keep',
    'QUANTITY': 'replace',
    'ORDINAL': 'ignore',
    'PERCENT': 'replace',
    'NORP': 'keep',
    'MONEY': 'replace',
    'LOC': 'ignore',
    'FAC': 'keep',
    'LANGUAGE': 'ignore',
    'EVENT': 'ignore',
    'LAW': 'ignore'
}

TAGS_TO_KEEP = {
    'IN', 'JJ', 'JJR', 'JJS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'RB', 'RBR',
    'RBS', 'RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB'
}

class ProcessWithSpacy(Task):

    def __init__(self, spacyModelName, *args, **kwargs):
        super(ProcessWithSpacy, self).__init__(*args, **kwargs)
        self.spacyModelName = spacyModelName
        # self.k=0

    def init(self):
        self.spacyModel = spacy.load(self.spacyModelName)

    def run(self, comment):
        # self.k+=1
        # if self.k % 1000 != 0:
        #     return
        spacyDocument = self.spacyModel(comment.text)
        labels={f'hn{comment.hid}', f'@{comment.author}'}
        if comment.parent != -sys.maxsize:
            labels.add(f'hn{comment.parent}')
        with spacyDocument.retokenize() as retokenizer:
            for entity in spacyDocument.ents:
                if NER_CHANGES[entity.label_] == 'replace':
                    span=spacyDocument[entity.start:entity.end]
                    retokenizer.merge(span, attrs={"TAG": "IGNORE"})
                if NER_CHANGES[entity.label_] == 'keep':
                    labels.add(entity.text.lower())
        tokens = [token.lemma_.lower() for token in spacyDocument if token.tag_ in TAGS_TO_KEEP]
        self.output.append(Document(
            hid=comment.hid,
            timestamp=comment.timestamp,
            tokens=tokens,
            labels=list(labels)
        ))
