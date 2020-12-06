import sys
import spacy
from hypergol import Task
from data_models.document import Document

# replace -> swap the sf with the type
# keep -> extract NER as a label
# ignore -> do nothing
NER_CHANGES = {
    'CARDINAL': 'one',
    'PERSON': 'keep',
    'TIME': 'ten hours',
    'WORK_OF_ART': 'keep',
    'ORG': 'keep',
    'DATE': 'today',
    'GPE': 'keep',
    'PRODUCT': 'keep',
    'QUANTITY': '100 watts',
    'ORDINAL': 'first',
    'PERCENT': '100%',
    'NORP': 'keep',
    'MONEY': '$100',
    'LOC': 'ignore',
    'FAC': 'keep',
    'LANGUAGE': 'ignore',
    'EVENT': 'ignore',
    'LAW': 'ignore'
}

class ProcessWithSpacy(Task):

    def __init__(self, spacyModelName, *args, **kwargs):
        super(ProcessWithSpacy, self).__init__(*args, **kwargs)
        self.spacyModelName = spacyModelName

    def init(self):
        self.spacyModel = spacy.load(self.spacyModelName)

    def run(self, comment):
        text = comment.text
        spacyDocument = spacyModel(text)
        labels=[f'H{comment.hid}', f'@{comment.author}']
        if comment.parent != -sys.maxsize:
            labels.append(f'H{comment.parent}')
        for entity in spacyDocument.ents:
            if NER_CHANGES[entity.label_] not in ['keep', 'ignore'] and text[entity.start_char:entity.end_char] == entity.text:
                text = text[:entity.start_char] + NER_CHANGES[entity.label_] + text[entity.end_char:]
            if NER_CHANGES[entity.label_] == 'keep':
                labels.append(entity.text)
        modifiedSpacyDocument = spacyModel(text)


        self.output.append(Document(
            hid=comment.hid,
            timestamp=comment.timestamp,
            tokens=tokens,
            labels=labels
        ))
