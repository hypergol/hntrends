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
    'NN', 'JJ', 'VB', 'NNS', 'NNP', 'VBP', 'VBG', 'VBN', 'VBD', 'JJR', 
    'RBR', 'JJS', 'PDT', 'NNPS', 'RBS'
}

class ProcessWithSpacy(Task):

    def __init__(self, logAtEachN, spacyModelName, *args, **kwargs):
        super(ProcessWithSpacy, self).__init__(*args, **kwargs)
        self.spacyModelName = spacyModelName
        self.logAtEachN = logAtEachN
        self.cnt = 0

    def init(self):
        self.spacyModel = spacy.load(self.spacyModelName)

    def run(self, comment):
        self.cnt += 1
        if self.cnt % self.logAtEachN == 0:
            self.logger.log(f'Processed: {self.cnt}')
        spacyDocument = self.spacyModel(comment.text)
        labels=[f'H{comment.hid}', f'@{comment.author}']
        if comment.parent != -sys.maxsize:
            labels.append(f'H{comment.parent}')
        with spacyDocument.retokenize() as retokenizer:
            for entity in spacyDocument.ents:
                if NER_CHANGES[entity.label_] == 'replace':
                    span=spacyDocument[entity.start:entity.end]
                    retokenizer.merge(span, attrs={"TAG": "XXX"})
            if NER_CHANGES[entity.label_] == 'keep':
                labels.append(entity.text)
        tokens = [token.lemma_ for token in spacyDocument if token.tag_ in TAGS_TO_KEEP]
        self.output.append(Document(
            hid=comment.hid,
            timestamp=comment.timestamp,
            tokens=tokens,
            labels=labels
        ))
