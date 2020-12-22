import fire
from hypergol import HypergolProject
from hypergol import Pipeline
from tasks.create_elements import CreateElements
from tasks.create_cluster_models import CreateClusterModels
from data_models.document import Document
from data_models.element import Element


def create_clusters(threads=1, force=False):
    project = HypergolProject(dataDirectory='.', force=force)
    documents = project.datasetFactory.get(
        dataType=Document, 
        branch='document_creation', 
        name='documents', 
        chunkCount=256
    )
    elements = project.datasetFactory.get(
        dataType=Element, 
        name='elements', 
        chunkCount=256
    )

    createElements = CreateElements(
        inputDatasets=[documents],
        outputDataset=elements,
        debug=True
    )
    createClusterModels = CreateClusterModels(
        loadedInputDatasets=[elements],
        outputDataset=exampleOutputDataset,
    )

    pipeline = Pipeline(
        tasks=[
            createElements,
            createClusterModels,
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(create_clusters)
