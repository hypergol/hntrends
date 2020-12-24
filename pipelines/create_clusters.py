import fire
from hypergol import HypergolProject
from hypergol import Pipeline
from tasks.create_elements import CreateElements
from tasks.create_cluster_models import CreateClusterModels
from data_models.document import Document
from data_models.element import Element
from data_models.cluster_model import ClusterModel


class EpochSaver:
    pass


def create_clusters(dataDirectory, threads=1, force=False):
    project = HypergolProject(dataDirectory=dataDirectory, force=force)
    documents = project.datasetFactory.get(
        dataType=Document, 
        branch='document_creation', 
        name='documents', 
        chunkCount=256
    )
    elements = project.datasetFactory.get(
        dataType=Element, 
        name='elements', 
        chunkCount=16
    )
    clusterModels = project.datasetFactory.get(
        dataType=ClusterModel,
        name='cluster_models',
        chunkCount=256
    )

    createElements = CreateElements(
        inputDatasets=[documents],
        outputDataset=elements,
        modelPath='/mnt/ds/doc2vec/doc2vec_20201213_c0c6fccadce4d1cad0eb3aa93bff9ac20fa81cda_015.model',
        logAtEachN=10_000,
        debug=True
    )
    createClusterModels = CreateClusterModels(
        loadedInputDatasets=[elements],
        outputDataset=clusterModels,
        logAtEachN=10,
        debug=True
    )

    pipeline = Pipeline(
        tasks=[
            createElements,
            # createClusterModels,
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(create_clusters)
