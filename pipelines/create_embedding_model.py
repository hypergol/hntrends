import os
import fire
import requests
from itertools import islice
from datetime import date
from tqdm import tqdm
from data_models.document import Document
from hypergol import Logger
from hypergol import HypergolProject
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import Doc2Vec
from gensim.models.callbacks import CallbackAny2Vec

VECTOR_SIZE = 100

def slack_message(message)
    response = requests.post(
        url=os.environ['LC_PERSONAL_SLACK'],
        headers={'Content-type': 'application/json'},
        data=f'{{"text":"{message}"}}'
    )

class EpochSaver(CallbackAny2Vec):

    def __init__(self, modelDirectory, modelName=None, epoch=0):
        self.modelDirectory = modelDirectory
        self.modelName = modelName or 'doc2vec'
        self.epoch = epoch

    def on_epoch_end(self, model):
        slack_message(message=f'Saving epoch:{self.epoch:03}')
        model.save(f'{self.modelDirectory}/{self.modelName}_{self.epoch:03}.model')
        self.epoch += 1

def create_embedding_model(sourceDataDirectory, modelDirectory, loadModelFile=None, threads=1, force=False): 
    slack_message(message='Processing start')
    logger = Logger()
    project = HypergolProject(dataDirectory=sourceDataDirectory, force=force)
    documents = project.datasetFactory.get(
        dataType=Document, 
        branch='document_creation', 
        name='documents', 
        chunkCount=256
    )

    logger.info('Loading dataset - START')
    taggedData = []
    with documents.open('r') as dsr:
        for document in tqdm(dsr, total=21_000_000):
        # for document in tqdm(islice(dsr, 100_000), total=100_000):
            taggedData.append(TaggedDocument(words=document.tokens, tags=document.labels))
    logger.info('Loading dataset - END')

    modelName = f'doc2vec_{date.today().strftime("%Y%m%d")}_{project.repoManager.commitHash}'
    if loadModelFile is None:
        logger.info('Model construction - START')
        model = Doc2Vec(
            dm=0, dbow_words=1, dm_concat=0, vector_size=VECTOR_SIZE, window=5, 
            negative=20, hs=0, min_count=3, workers=31, 
            epochs=50, alpha=0.025, min_alpha=0.001, 
            callbacks=[
                EpochSaver(
                    modelDirectory=modelDirectory, 
                    modelName=modelName
                )
            ]
        )
        model.build_vocab(taggedData)
        logger.info('Model construction - END')
    else:
        logger.info('Model loading - START')
        model = Doc2Vec.load(loadModelFile)
        model.callbacks=[
            EpochSaver(
                modelDirectory=modelDirectory,
                modelName=modelName,
                epoch=model.callbacks[0].epoch + 1
            )
        ]
        logger.info('Model loading - END')

    logger.info('Model training - START')
    model.train(documents=taggedData, total_examples=model.corpus_count, epochs=model.epochs)
    logger.info('Model training - END')

if __name__ == '__main__':
    fire.Fire(create_embedding_model)
