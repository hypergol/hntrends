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

class ProcessWithSpacy(Task):

    def __init__(self, spacyModelName, *args, **kwargs):
        super(ProcessWithSpacy, self).__init__(*args, **kwargs)
        self.spacyModelName = spacyModelName

    def init(self):
        self.spacyModel = spacy.load(self.spacyModelName)

    def run(self, comment):
        text = comment.text
        spacyDocument = spacyModel(text)
        for entity in spacyDocument.ents:




        raise NotImplementedError(f'{self.__class__.__name__} must implement run()')
        self.output.append(exampleOutputObject)
