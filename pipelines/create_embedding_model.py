import os
import fire
import logging
import array
import numpy as np
import scipy.sparse as sps
from datetime import date
from itertools import islice
from tqdm import tqdm

from data_models.document import Document
from hypergol import HypergolProject
from hypergol.logger import Logger

from gensim.models.callbacks import CallbackAny2Vec
from gensim.test.utils import get_tmpfile
from gensim.models.doc2vec import Doc2Vec


    
VECTOR_SIZE = 100

class EpochSaver(CallbackAny2Vec):

    def __init__(self, modelDirectory, modelName):
        self.modelDirectory = modelDirectory
        self.modelName = modelName
        self.epoch = 0

    def on_epoch_end(self, model):
        Path(self.modelDirectory).mkdir(parents=True, exist_ok=True)
        fileName = get_tmpfile(f'{self.modelDirectory}/{self.modelName}_{self.epoch:03}.model')
        model.save(fileName)
        self.epoch += 1

def create_vocabulary(documentsDataset, logger, dataDirectory):
    logger.info('Process documents - START')
    vocabulary = {}
    rows=array.array('I')
    cols=array.array('I')
    mentionId = 1_000_000_0000
    with documentsDataset.open('r') as dsr:
        # for document in tqdm(dsr, total=21_000_000):
        for document in tqdm(islice(dsr, 1_000_000), total=1_000_000):
            hid = f'hn{document.hid}'
            for label in document.labels:
                if label not in vocabulary:
                    vocabulary[label] = len(vocabulary)
                if label != hid:
                    rows.append(vocabulary[hid])
                    cols.append(vocabulary[label])
            lastMentionId = None
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)
                if lastMentionId is not None:
                    rows.append(lastMentionId)
                    cols.append(mentionId)
                rows.append(vocabulary[token])
                cols.append(mentionId)
                rows.append(mentionId)
                cols.append(vocabulary[hid])
                lastMentionId = mentionId
                mentionId += 1
    logger.info('Process documents - save vocabulary')
    pickle.dump(vocabulary, open(f'{dataDirectory}/vocabulary.pkl', 'rb'))
    logger.info('Process documents - save rows - END')
    np.save(f'{dataDirectory}/rows.npy', np.frombuffer(rows, dtype=np.int32))
    logger.info('Process documents - save cols - END')
    np.save(f'{dataDirectory}/cols.npy', np.frombuffer(cols, dtype=np.int32))
    logger.info('Process documents - END')

def create_embedding_model(sourceDataDirectory, dataDirectory, threads=1, force=False): 
    logger = Logger()
    project = HypergolProject(dataDirectory=sourceDataDirectory, force=force)
    documentsDataset = project.datasetFactory.get(
        dataType=Document, 
        branch='document_creation', 
        name='documents', 
        chunkCount=256
    )

    create_vocabulary(documentsDataset=documentsDataset, logger=logger, dataDirectory=dataDirectory)


    
    # epochSaver = EpochSaver(
    #     modelDirectory=project.datasetFactory.branchDirectory,
    #     modelName=f'doc2vec_{date.today().strftime("%Y%m%d")}_{project.repoManager.commitHash}'
    # )



    # logger.info('Model construction - START')
    # model = Doc2Vec(
    #     dm=0, dbow_words=1, dm_concat=0, vector_size=VECTOR_SIZE, window=5, 
    #     negative=20, hs=0, min_count=3, workers=31, 
    #     epochs=50, alpha=0.025, min_alpha=0.001, callbacks=[epochSaver]
    # )
    # model.build_vocab(taggedData)
    # logger.info('Model construction - END')

    # logger.info('Model training - START')
    # model.train(documents=taggedData, total_examples=model.corpus_count, epochs=model.epochs)
    # logger.info('Model training - END')

if __name__ == '__main__':
    fire.Fire(create_embedding_model)
