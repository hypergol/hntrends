import os
import fire
from hypergol import HypergolProject
from hypergol.hypergol_project import RepoManager
from hypergol import Pipeline
from tasks.load_data import LoadData
from tasks.select_stories import SelectStories
from tasks.select_comments import SelectComments
from tasks.process_with_spacy import ProcessWithSpacy
from data_models.raw_data import RawData
from data_models.comment import Comment
from data_models.story import Story
from data_models.document import Document

def process_hacker_news(filePattern, dataDirectory, threads=1, raiseIfDirty=True, force=False): 
    project = HypergolProject(
        dataDirectory=dataDirectory, 
        force=force,
        repoManager=RepoManager(repoDirectory=os.getcwd(), raiseIfDirty=raiseIfDirty)
    )
    rawData = project.datasetFactory.get(dataType=RawData, name='raw_data', chunkCount=256)
    comments = project.datasetFactory.get(dataType=Comment, name='comments', chunkCount=256)
    stories = project.datasetFactory.get(dataType=Story, name='stories', chunkCount=256)
    documents = project.datasetFactory.get(dataType=Document, name='documents', chunkCount=256)

    loadData = LoadData(
        logAtEachN=200_000,
        filePattern=filePattern,
        outputDataset=rawData
    )

    selectStories = SelectStories(
        inputDatasets=[rawData],
        outputDataset=stories,
    )
    selectComments = SelectComments(
        inputDatasets=[rawData],
        outputDataset=comments,
    )

    processWithSpacy = ProcessWithSpacy(
        logAtEachN=200_000,
        spacyModelName='en_core_web_sm',
        inputDatasets=[comments],
        outputDataset=documents,
    )

    pipeline = Pipeline(
        tasks=[
            # loadData,
            # selectStories,
            # selectComments,
            processWithSpacy
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(process_hacker_news)
