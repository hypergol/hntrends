import os
import fire
import logging
from tqdm import tqdm
from hypergol import HypergolProject
from hypergol.logger import Logger
from gensim.models.doc2vec import TaggedDocument

from gensim.models.callbacks import CallbackAny2Vec
from gensim.test.utils import get_tmpfile
from gensim.models.doc2vec import Doc2Vec
    
VECTOR_SIZE = 100

class EpochSaver(CallbackAny2Vec):

    def __init__(self, modelDirectory):
        self.modelDirectory = modelDirectory
        self.epoch = 0

    def on_epoch_end(self, model):
        fileName = get_tmpfile(f'{self.modelDirectory}/doc2vec_{self.epoch:03}.model')
        model.save(fileName)
        self.epoch += 1


def train_embedding_model(filePattern, dataDirectory, threads=1, raiseIfDirty=True, force=False): 
    logger = Logger()
    project = HypergolProject(
        dataDirectory=dataDirectory, 
        force=force,
        repoManager=RepoManager(repoDirectory=os.getcwd(), raiseIfDirty=raiseIfDirty)
    )
    modelDirectory = f'{}/{}/{}'
    modelDirectory = '/data/doc2vec'
    documents = project.datasetFactory.get(
        dataType=Document, 
        branch='document_creation', 
        name='documents', 
        chunkCount=256
    )
    epochSaver = EpochSaver(modelDirectory=modelDirectory)

    logger.info('Loading dataset - START')
    taggedData = []
    with documents.open('r') as dsr:
        for v in tqdm(dsr, total=21_000_000):
            taggedData.append(TaggedDocument(words=v.tokens, tags=v.labels))
    logger.info('Loading dataset - END')

    logger.info('Model construction - START')
    model = Doc2Vec(
        dm=0, dbow_words=1, dm_concat=0, vector_size=VECTOR_SIZE, window=5, 
        negative=20, hs=0, min_count=3, workers=31, 
        epochs=50, alpha=0.025, min_alpha=0.001, callbacks=[epochSaver]
    )
    model.build_vocab(taggedData)
    logger.info('Model construction - END')

    logger.info('Model training - START')
    model.train(documents=taggedData, total_examples=model.corpus_count, epochs=model.epochs)
    logger.info('Model training - END')


if __name__ == '__main__':
    fire.Fire(train_embedding_model)
